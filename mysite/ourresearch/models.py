
# Create your models here.
from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey


from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index


# class FontAwesomeSizeBlock(blocks.ChoiceBlock):
#     choices = [
#         ('fa-lg'),
#         ('fa-2x'),
#         ('fa-3x'),
#         ('fa-4x'),
#         ('fa-5x'),
#     ]
#
#     class Meta:
#         icon = 'plus'


# class OurResearchIndexThumb(blocks.StructBlock):
#     fa_icon = blocks.CharBlock()
#     fa_icon_size = FontAwesomeSizeBlock()
#     caption = blocks.CharBlock()
#
#     class Meta:
#         icon = 'image'
#         template = 'blocks/our_research_index_thumb.html'


class OurResearchIndex(Page):
    intro_index = models.CharField(max_length=500, blank=True)
    # subject = StreamField([('subject', OurResearchIndexThumb())])

    content_panels = Page.content_panels + [
        FieldPanel('intro_index'),
        # StreamFieldPanel('subject'),
        ]


class OurResearchSubject(Page):
    intro = models.CharField(max_length=500, blank=True)
    fa_icon_subject = models.CharField(max_length=255, default="fa-")
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('fa_icon_subject')
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

