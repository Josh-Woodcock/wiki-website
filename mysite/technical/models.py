from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index

from django.db import models


# Create your models here.


class TechnicalPage(Page):

    description = models.CharField(max_length=500, blank=True)
    body = StreamField([
        ('section_heading', blocks.CharBlock(classname="full title")),
        ('sub_section_heading', blocks.CharBlock()),
        ('text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]