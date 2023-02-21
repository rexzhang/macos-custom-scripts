# Alfred Workflow: Time Converter

[![downloads](https://img.shields.io/github/downloads/rexzhang/alfred-workflow-time-converter/total)](https://github.com/rexzhang/asgi-webdav/releases)

## What

![demo-basic](docs/demo-basic.gif)

## How

### Change Time Zone

```
now +08
```

### Time Shift

```
now +1d
now -1w
```

| key | unit                           |                           
|-----|--------------------------------|
| ms  | microseconds(not support yest) | 
| s   | seconds                        |
| m   | minutes                        |
| h   | hours                          |
| d   | days                           |
| w   | weeks                          |                          
| M   | months                         |                       
| q   | quarters(not support yest)     |     
| y   | years                          |                          

## Depend

- Python3.9+

## Get it

Download
from [GitHub release](https://github.com/rexzhang/alfred-workflow-time-converter/releases)
, double click package file to install.

## History

### 0.3.0

- support python3

### 0.2.0

- support time zone
- support time shift

### 0.1.0

- first release

## Todo

- multi time shift args?
- time shift support ms/q
