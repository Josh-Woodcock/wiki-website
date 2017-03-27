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

# Create your models here.


class QandABlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, max_length=255)
    answer = blocks.RichTextBlock()

    class Meta:
        icon = 'help'
        label = 'Question and Answer'
        template = 'blocks/QandABlock.html'


class FAQ(Page):
    intro = RichTextField(blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('question_and_answer', QandABlock()),

    ])

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        StreamFieldPanel('body'),
    ]

