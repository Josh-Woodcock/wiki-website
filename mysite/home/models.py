from __future__ import absolute_import, unicode_literals

from django.db import models

from django import forms
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from wagtail.wagtailcore.models import Page


class CarouselBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=True, max_length=255)
    text = blocks.RichTextBlock()
    link = blocks.PageChooserBlock()

    class Meta:
        icon = 'site'
        label = 'Carousel Block'
        template = 'blocks/CarouselBlock.html'


class HomePage(Page):
    body = StreamField([
        ('Carousel', CarouselBlock()),
    ], null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
