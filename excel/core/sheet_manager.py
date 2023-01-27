import gspread
import datetime

from gspread import WorksheetNotFound

from django.conf  import settings


gc = gspread.service_account_from_dict(settings.GOOGLE_AUTH_DICT)


class SheetManager:
    def __init__(self, user):
        self.user = user
        if self.user.working_sheet_key:
            self.working_sheet = gc.open_by_key(user.working_sheet_key)
        else:
            name = f"{user.first_name}'s" or f"{user.handle}'s" or 'Your'
            name += " Budget Dashboard"
            self.working_sheet = gc.create(name)
            self.user.working_sheet_key = self.working_sheet.id
            self.user.save()

    def __create_or_get_sheet_by_user(self, sheet_name):
        """
        Check if a sheet with the given name already exists in the spreadsheet.
        If it does not exist, create a new sheet with that name.
        Returns the worksheet.
        """
        try:
            return self.working_sheet.worksheet(sheet_name)
        except WorksheetNotFound:
            return self.working_sheet.add_worksheet(title=sheet_name, rows=None, cols=None)

    def create_or_get_sheet_by_month(self, date_time=None, clean=False):
        month = date_time or datetime.datetime.now().strftime("%B")
        name = self.user.username or self.user.first_name or self.user.user_id
        sheet_name = f'{name} [{month}]'
        sheet = self.__create_or_get_sheet_by_user(sheet_name)
        if clean:
            sheet.clear()
        return sheet

    def share(self, email_address=None):
        if email_address:
            self.working_sheet.share(email_address, perm_type='user', role='writer')
        elif self.user.email:
            self.working_sheet.share(self.user.email, perm_type='user', role='writer')
        else:
            raise Exception('Provide an email address!')


