import requests
import json


class Gecko(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def push(self, widget):
        widget.validate()
        response = requests.post(
            'https://push.geckoboard.com/v1/send/%s' % widget.key,
            json.dumps({'api_key' : self.api_key, 'data' : widget.data()}),
            verify=False
        )
        response.raise_for_status()
        if not response.json().get('success') == True:
            raise ValueError(response.content)


class Widget(object):
    def __init__(self, widget_key):
        self._key = widget_key
        self._items = []

    @property
    def key(self):
        return self._key

    def validate(self):
        pass

    def data(self):
        raise ValueError('No data exposed from this widget')


class Funnel(Widget):
    # https://developer.geckoboard.com/#funnel

    class Order:
        STANDARD = 0
        REVERSE = 1

    def __init__(self, widget_key):
        super(Funnel, self).__init__(widget_key)
        self.set_order(Funnel.Order.STANDARD)
        self.show_percentage(True)

    def set_order(self, value):
        self._order = value

    def show_percentage(self, value):
        self._show_percentage = value

    def add_item(self, label, value):
        self._items.append({'label': label, 'value': float(value)})

    def add_items(self, tuples):
        for key, value in tuples:
            self.add_item(key, value)

    def data(self):
        data = {
            'item': self._items
        }

        if self._order == Funnel.Order.REVERSE:
            data['type'] = 'reverse'

        if self._show_percentage == False:
            data['percentage'] = 'hide'

        return data


class NumberWidget(Widget):
    # https://developer.geckoboard.com/#number-and-secondary-stat

    def __init__(self, widget_key):
        super(NumberWidget, self).__init__(widget_key)

    def add_stat(self, number1, number2 = None, text = None):
        if number1 is not None: self._items.append({'text': text, 'value': number1})
        if number2 is not None: self._items.append({'text': text, 'value': number2})

    def spark_line(self, values = []):
        self._items.append(values)

    def data(self):
        return {
            'item': self._items
        }


class GeckOMeterWidget(Widget):
    # https://developer.geckoboard.com/#geck-o-meter

    def set_stat(self, value, min, max, min_text='', max_text=''):
        self.current_value = value
        self.min_value = min
        self.max_value = max
        self.min_text = min_text
        self.max_text = max_text

    def data(self):
        return {
            'item': float(self.current_value),
            'min' : {
                'value': float(self.min_value),
                'text' : self.min_text
            },
            'max' : {
                'value': float(self.max_value),
                'text' : self.max_text
            }
        }


class RAG(Widget):
    # https://developer.geckoboard.com/#rag

    def add_item(self, text, value):
        self._items.append({'text': text, 'value': float(value)})

    def validate(self):
        if len(self._items) < 2 or len(self._items) > 3:
            raise ValueError('The RAG widget expects 2 or 3 items.')

    def data(self):
        return {
            'item': self._items
        }


class PieChart(Widget):
    # https://developer.geckoboard.com/#pie-chart

    def add_item(self, label, value, color=None):
        self._items.append({'label': label, 'value': value, 'color' : color})

    def add_items(self, tuples):
        for key, value in tuples:
            self.add_item(key, value)

    def validate(self):
        if len(self._items) < 1:
            raise ValueError('We need at least 1 items for PieChart')

    def data(self):
        return {
            'item': self._items
        }


class Text(Widget):
    # https://developer.geckoboard.com/#text

    class Type:
        DEFAULT = 0
        ALERT = 1
        INFO = 2

    def add_item(self, text, type=Type.DEFAULT):
        self._items.append({'text': text, 'type': type})

    def data(self):
        return {
            'item': self._items
        }
