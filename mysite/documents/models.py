from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel

from wagtail.wagtailsearch import index
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from django.db import models


# Create your models here.

# class Document(blocks.StructBlock):
#     title = blocks.CharBlock(),
#     document = DocumentChooserBlock()


class DocumentPage(Page):
    description = models.CharField(max_length=500, blank=True)
    body = StreamField([
        ('section_heading', blocks.CharBlock(classname="full title")),
        ('document', DocumentChooserBlock())
        ])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]