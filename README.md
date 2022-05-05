# Importante
- para windows recomendo seguir: https://techzizou.com/yolo-installation-on-windows-and-linux/
## Requirements
- GCC
- Pytorch: https://pytorch.org/get-started/locally/
- Python 3
- Darknet
- OpenCV
- Pip

Para instalar os pacotes pip:
```
pip install -r requirements.txt
```

Para instalar Darknet:
```
git clone https://github.com/pjreddie/darknet.git
cd darknet
make
```

Para usarmos o modelo com uma stream RTSP é necessário termos OPENCV instalado na máquina
- Tutorial para windows: https://docs.opencv.org/4.x/d5/de5/tutorial_py_setup_in_windows.html

- Tutorial para Linux:
https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html

Agora para ativar o OPENCV, no **Makefile** da Darknet mude a segunda linha OPENCV=0 para:
```
OPENCV=1
```

Finalmente, o modelo de reconhecimento usa os pesos e nomes fvlpd, apenas coloque todos os arquivos **fvlpd*** no diretório Darknet criado.