from django.db import models

class Currency(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)
    initials = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюти'

class AccountCategory(models.Model):
    category_name = models.CharField(max_length=50, blank=False, null=False)
    icon_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'Категорія рахунків'
        verbose_name_plural = 'Категорії рахунків'

class IncomeCategory(models.Model):
    category_name = models.CharField(max_length=50, blank=False, null=False)
    icon_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'Категорія доходів'
        verbose_name_plural = 'Категорії доходів'

class ExpenseCategory(models.Model):
    category_name = models.CharField(max_length=50, blank=False, null=False)
    icon_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'Категорія витрат'
        verbose_name_plural = 'Категорії витрат'


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    pdf = models.FileField(upload_to='pdfs/', blank=False, null=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'