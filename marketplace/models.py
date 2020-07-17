from django.db import models

# Create your models here.

class Book(models.Model):
    isbn = models.CharField(max_length=20) # TODO: Create custom Field type for ISBN
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    year = models.IntegerField(default=0)
    language = models.CharField(max_length=200)
    cover_img = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def get_cover_img_path(self):
        if not self.cover_img or self.cover_img == '':
            return "/static/marketplace/images/default_book.png"
        else:
            return self.cover_img

class University(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Programme(models.Model):
    name = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField(default=0)
    term = models.IntegerField(default=0)

    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    semesters = models.ManyToManyField(Semester)
    books = models.ManyToManyField(Book)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name