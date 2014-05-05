import requests, json

class Gecko(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def push(self, widget):
        widget._validate()
        ret = requests.post("https://push.geckoboard.com/v1/send/%s" % widget.widgetKey(), json.dumps({'api_key' : self.api_key, 'data' : widget.data()}), verify=False)
        if not (ret.status_code == 200 and ret.json().get('success') == True):
            raise ValueError(ret.content)

class Push:
    def widgetKey(self):
        return self.widget_key

    def _validate(self):
        raise NotImplementedError("No validation found for this Widget")

    def data(self):
        raise ValueError("No data exposed from this Widget")

class Funnel(Push):
    def __init__(self, widget_key):
        self.items = []
        self.standardOrder()
        self.showPercentage()
        self.widget_key = widget_key

    # Default
    def standardOrder(self):
        self.type = "standard"

    def reverseOrder(self):
        self.type = "reverse"

    # Default
    def showPercentage(self):
        self.percentage = "show"

    def hidePercentage(self):
        self.percentage = "hide"

    def addItem(self, label, value):
        self.items.append({"label": label, "value": value})

    def _validate(self):
        if len(self.items) < 3:
            raise ValueError("We need atleast 3 items for Funnel")

    def data(self):
        return {
            "type": self.type, 
            "percentage": self.percentage,
            "item": self.items
        }

class Text(Push):
    def __init__(self, widget_key):
        self.widget_key = widget_key
        self.items = []

    def addText(self, text):
        self._addText(text, 0)

    def addAlertText(self, text):
        self._addText(text, 1)

    def addInfoText(self, text):
        self._addText(text, 2)

    def _addText(self, text, _type):
        self.items.append({"text": text, "type": _type})

    def _validate(self):
        pass

    def data(self):
        return {
            "item": self.items
        }

class NumberWidget(Push):
    def __init__(self, widget_key):
        self.widget_key = widget_key
        self.items = []

    def addStat(self, number1, number2 = None, prefix = None):
        if number1: self.items.append({"text": prefix, "value": number1})
        if number2: self.items.append({"text": prefix, "value": number2})

    def sparkLine(self, values = []):
        self.items.append(values)

    def _validate(self):
        pass

    def data(self):
        return {
            "item": self.items
        }
