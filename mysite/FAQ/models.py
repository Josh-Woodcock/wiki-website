from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index


# Create your models here.


class QandABlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, max_length=255)
    answer = blocks.RichTextBlock()

    class Meta:
        icon = 'help'
        label = 'Question and Answer'
        template = 'blocks/QandABlock.html'


class FAQ(Page):
    intro = models.CharField(max_length=500, blank=True)
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

