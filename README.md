Foreground extraction model.

## Getting started
```bash
sudo apt-get update
sudo apt-get install python3.7
sudo apt-get install python-virtualenv

cd titlematch/
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install python3.7-tk
```

## Example
```bash
python main.py -h
python main.py --input='images/input/photo_2019-02-12_15-54-31.jpg'\
               --output='images/output'
               --show=True
```

## Results
![Before](images/input/photo_2019-02-12_15-54-31.jpg) ![After](images/output/photo_2019-02-12_15-54-31_fg.jpg)
---------------------------
![Before](images/input/photo_2019-02-12_12-43-20.jpg) ![After](images/output/photo_2019-02-12_12-43-20_fg.jpg)
---------------------------
![Before](images/input/photo_2019-02-12_12-43-26.jpg) ![After](images/output/photo_2019-02-12_12-43-26_fg.jpg)
---------------------------
![Before](images/input/photo_2019-02-12_15-54-36.jpg) ![After](images/output/photo_2019-02-12_15-54-36_fg.jpg)
---------------------------
![Before](images/input/photo_2019-02-12_15-54-41.jpg) ![After](images/output/photo_2019-02-12_15-54-41_fg.jpg)
