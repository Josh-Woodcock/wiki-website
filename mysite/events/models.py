from django import forms
from datetime import date

from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index

from wagtail.contrib.table_block.blocks import TableBlock

# PAGE MODELS


class EventIndexPage(Page):
    intro = models.CharField(max_length=500, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")

    ]


class EventPageTag(TaggedItemBase):
    content_object = ParentalKey('EventPage', related_name='tagged_items')


class EventPage(Page):
    organiser = models.CharField(max_length=255)
    date = models.DateField(("Date"), default=date.today)
    start_time = models.TimeField("Start Time", default='10:00')
    end_time = models.TimeField(("End Time"), default='17:00')
    location = models.CharField(max_length=255)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
    ])
    tags = ClusterTaggableManager(through=EventPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        MultiFieldPanel([
        FieldPanel('organiser'),
        FieldPanel('date'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('location'),
        FieldPanel('tags'),
    ], heading="Event Information"),
        InlinePanel('gallery_images', label="Event Image"),
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('date'),
        index.SearchField('location'),
        index.SearchField('tags'),

    ]


class EventPageGalleryImage(Orderable):
    page = ParentalKey(EventPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

