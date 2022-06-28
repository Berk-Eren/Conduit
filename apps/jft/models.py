from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )

    def __str__(self):
        return self.name

class Invitation(models.Model):
    name = models.CharField(max_length=30)
    """invitation = models.ManyToManyField(
        Person,
        through="Relation",
        related_name="testing"
    )
    """

class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)

class Relation(models.Model):
    name = models.CharField(max_length=50)