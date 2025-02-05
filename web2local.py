class pybind11_path(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import imp, os
        try:
            imp.find_module('pybind11')
        except ImportError:
            os.system('pip install pybind11')

        import pybind11
        return pybind11.get_include(self.user)


class web2local(object):
    def __init__(self,
        from_url,
        to_local,
        extract_to,
        extract_method,
        using_user_home=False):

        import os,tarfile,zipfile
        from urllib.request import Request, urlopen
        from pathlib import Path

        root = Path.cwd()
        if using_user_home:
            root = Path.home()

        if not os.path.exists(root / to_local):
            os.makedirs(root / to_local)

        filename = Path(from_url).name
        filepath = root/to_local/filename

        if not os.path.exists(filepath):
            #req = Request(from_url, headers={'User-Agent': 'Mozilla/5.0'})
            #tarobj = urlopen(req).read()
            #with open(filepath, 'wb') as f:
            #    f.write(tarobj)
            import requests

            #target_path = 'boost.tar.gz'

            response = requests.get(from_url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.raw.read())

        extract_folderpath = root / to_local

        if not os.path.exists(root / to_local / extract_to):
            print('Extracting to:', extract_folderpath)
            if extract_method == 'gz':
                tf = tarfile.open(filepath)
                tf.extractall(path=extract_folderpath)
            elif extract_method == 'zip':
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(extract_folderpath)

        folderpath = extract_folderpath /extract_to
        self.folderpath = str(folderpath)

    def __str__(self):
        return self.folderpath

if __name__ == "__main__":
    path = web2local(
        from_url='https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz',
        to_local='external',
        extract_to='eigen-3.3.7',
        extract_method='gz'
    )
    print(path)