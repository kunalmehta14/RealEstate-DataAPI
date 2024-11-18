class APIRouter:
  def db_for_read(self, model, **hints):
     if model._meta.app_label == 'realestate_data_api':
        return 'Ontario'
     return None