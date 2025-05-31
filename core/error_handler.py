
def validation_error(e):
    '''Return a custom message and 422 status code'''
    return { 'errors': e.messages }, 422

