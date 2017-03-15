from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index

from wagtail.contrib.table_block.blocks import TableBlock

# Create your models here.


class OurResearchIndex(Page):
    pass


class OurResearchSubject(Page):

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class OurResearchArticle(Page):
    researcher = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        MultiFieldPanel([
        FieldPanel('researcher'),
        FieldPanel('university'),
    ], heading="Research Information"),
        InlinePanel('gallery_images', label="Image Left"),
        StreamFieldPanel('body'),
    ]


    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('researcher'),
        index.SearchField('university'),
    ]


class OurResearchGalleryImage(Orderable):
    page = ParentalKey(OurResearchArticle, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]