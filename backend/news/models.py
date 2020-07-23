from django.db import models
from wagtail.admin import blocks
from wagtail.api import APIField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_headless_preview.models import HeadlessPreviewMixin


class NewsPage(HeadlessPreviewMixin, Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title", icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="pilcrow")),
            ("image", ImageChooserBlock(icon="image")),
        ]
    )
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        ImageChooserPanel("image"),
        StreamFieldPanel("body", classname="full"),
    ]

    api_fields = [
        APIField("date"),
        APIField("intro"),
        APIField("body"),
        APIField(
            "image_thumbnail",
            serializer=ImageRenditionField("fill-300x300", source="image"),
        ),
    ]
