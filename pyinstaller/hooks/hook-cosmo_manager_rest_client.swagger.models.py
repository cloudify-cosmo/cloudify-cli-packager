from cosmo_manager_rest_client.swagger import models

hiddenimports = ['{0}.{1}'.format(models.__package__, model)
                 for model in models.__all__]
