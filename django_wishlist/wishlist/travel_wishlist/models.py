from django.db import models

# Create your models here.


class Place(models.Model):
    # Model representing a place in the travel wishlist
    # Field to store the name of the place
    name = models.CharField(max_length=200)
    # Field to indicate whether the place has been visited or not
    visited = models.BooleanField(default=False)

    # Method to return a string representation of the object
    def __str__(self):
        # Return a string containing the name of the place and its visited status
        return f'{self.name}, visited? {self.visited}'