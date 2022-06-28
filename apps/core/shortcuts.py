from rest_framework import exceptions


def get_object_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except:
        excpt_msg = ("Object couldn't be found in"
                      "'{}' model".format(model.__class__.__name__)
                       + "with following parameters"
                        ", ".join(["{}={}".format(key, value)\
                                        for (key, value) in kwargs.items()]) )
        raise exceptions.NotFound(excpt_msg)