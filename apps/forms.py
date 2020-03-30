class FormMixin(object):
    def get_errors(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            news_errors = {}
            for key, message_dicts in errors.items():
                print(key)
                print(message_dicts)
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                news_errors[key] = messages
                print(news_errors)
            return news_errors
        else:
            return {}