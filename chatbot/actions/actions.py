# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionPrintInformation(Action):

    def name(self) -> Text:
        return "validate_newsletter_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        localisation = tracker.get_slot('localisation')
        area = tracker.get_slot('area')
        finishing_standard = tracker.get_slot('finishing_standard')

        print(localisation)
        print(area)
        print(finishing_standard)
        return []

class ActionPsssInformation(Action):

    def name(self) -> Text:
        return "submit_newsletter_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        localisation = tracker.get_slot('localisation')
        area = tracker.get_slot('area')
        number_of_rooms = tracker.get_slot('number_of_rooms')
        finishing_standard = tracker.get_slot('finishing_standard')
        floor = tracker.get_slot('floor')
        # SlotSet(localisation,None) 
        # SlotSet(area,None)

        print(localisation)
        print(area)
        print(number_of_rooms)
        print(finishing_standard)
        print(floor)
        return []
        
