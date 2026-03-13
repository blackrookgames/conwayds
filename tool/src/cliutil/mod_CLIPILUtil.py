__all__ = [\
    'CLIPILUtil',]

from PIL import\
    Image as _Image

from .mod_CLICommandError import\
    CLICommandError as _CLICommandError

class CLIPILUtil:
    """
    CLI-utility for PIL-related operations
    """
    
    #region image

    @classmethod
    def image_from_file(cls, path:str):
        """
        Loads an Image from a file
        
        :param path:
            Path of input file
        :return:
            Loaded Image
        :raise CLICommandError:
            An error occurred
        """
        try:
            with _Image.open(path) as image:
                image.load()
                return image
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    @classmethod
    def image_to_file(cls, image:_Image.Image, path:str):
        """
        Saves an Image to a file
        
        :param image:
            Image to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        try:
            image.save(path)
            return
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    #endregion