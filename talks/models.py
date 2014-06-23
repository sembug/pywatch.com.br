# -*- coding:utf-8 -*-

# Core Django imports
from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

# Thirdy Apps imports
from mptt.models import MPTTModel, TreeForeignKey

# Realative imports of the 'app-name' package
from core.models import TimeStampedModel, StandardItemStuffModel,\
    Media
from .managers import TalkManager


class Event(MPTTModel, TimeStampedModel):
    """
    Model reponsável por cadastrar os eventos
    e podem conter várias palestras.
    """

    parent = TreeForeignKey(
        'self',
        verbose_name=_(u'Evento Pai'),
        null=True,
        blank=True,
        related_name='children'
    )
    """
    Atributo da classe  para identificar um evento
    é pai de outro evento utilizando a estrutura
    de uma arvore mptt

    Caracteristicas:
    TreeForeignKey
    verbose name: Evento pai
    """

    name = models.CharField(
        verbose_name=_(u'Nome'),
        max_length=255
    )
    """
    Atributo da classe  para identificar um evento
    e seu nome

    Caracteristicas:
    CharField
    verbose name: Nome
    max length: 255
    """

    slug = models.SlugField(
        verbose_name=_(u'Slug'),
        max_length=255,
        unique=True,
        null=True
    )
    """
    Atributo da classe para criar um slug baseado
    no nome do evento

    Caracteristicas:
    SlugField
    verbose name: Slug
    max length: 255
    """

    def save(self, *args,  **kwargs):
        """
        Customiza o metodo salvar da classe
        para guardar o slug do evento
        """
        from uuslug import uuslug as slugify
        if not self.parent:
            slug_str = "%s" % (self.name)
        else:
            slug_str = "%s %s" % (self.parent.name, self.name)

        self.slug = slugify(slug_str, instance=self)
        super(Event, self).save(**kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = _(u'Evento')
        verbose_name_plural = _(u'Eventos')

    def __unicode__(self):
        return u'%s%s' % ('-' * self.level, self.name)


class Talk(TimeStampedModel, StandardItemStuffModel):
    """
    Model responsavel pelos palestras
    e pode ser associada a um evento
    """

    event = models.ForeignKey(
        Event,
        verbose_name=_(u'Evento'),
        blank=True,
        null=True
    )
    """
    Atributo da classe Talk para
    referenciar um objeto da classe Event

    Caracteristicas:
    ForeignKey
    verbose name: Evento
    """

    objects = TalkManager()

    def get_absolute_url(self):
        """
        Retorna o caminho absoluto da instancia
        do objeto, através do reverse
        usando namespace definido no arquivo
        urls.py
        """
        return reverse('talks:talk-detail-view', args=[self.slug])

    class Meta:
        ordering = ['created']
        verbose_name = _(u'Palestras')
        verbose_name_plural = _(u'Palestras')

    def __unicode__(self):
        return u'%s' % (self.title)


class MediaTalk(Media):
    """
    Model responsavel por criar as medias
    de palestrantes
    """

    talk = models.ForeignKey(
        'Talk',
        verbose_name=_(u'Palestras'),
        related_name='medias'
    )

    """
    Atributo da classe MediaTalk para referenciar
    ao objeto da classe Talk
    """

    class Meta:
        ordering = ['created']
        verbose_name = _(u'Media Palestrante')
        verbose_name_plural = _(u'Medias Palestrantes')

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.url)
