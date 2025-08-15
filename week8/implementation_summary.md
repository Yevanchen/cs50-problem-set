# Geolocation API 实现位置

## 1. 浏览器源码实现

### Chrome/Edge (Chromium)
- **源码位置**: `third_party/blink/renderer/modules/geolocation/geolocation.cc`
- **实现语言**: C++
- **GitHub链接**: https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/modules/geolocation/

```cpp
// Chromium 实际源码片段
void Geolocation::getCurrentPosition(V8PositionCallback* success_callback,
                                   V8PositionErrorCallback* error_callback,
                                   GeolocationPositionOptions* options) {
    // 实际的C++实现代码
    geolocation_service_->GetCurrentPosition(callback);
}
```

### Firefox
- **源码位置**: `dom/geolocation/Geolocation.cpp`
- **GitHub链接**: https://github.com/mozilla/gecko-dev/tree/master/dom/geolocation

### Safari (WebKit)  
- **源码位置**: `Source/WebCore/Modules/geolocation/Geolocation.cpp`
- **GitHub链接**: https://github.com/WebKit/WebKit/tree/main/Source/WebCore/Modules/geolocation

## 2. 操作系统API调用

### macOS
```objc
// Core Location Framework
#import <CoreLocation/CoreLocation.h>
CLLocationManager *locationManager = [[CLLocationManager alloc] init];
[locationManager requestLocation];
```

### Windows
```cpp
// Windows Location API  
#include <locationapi.h>
ILocation* pLocation = NULL;
CoCreateInstance(CLSID_Location, ...);
```

### Linux
```c
// GeoClue D-Bus API
dbus_g_proxy_call(proxy, "GetPosition", ...);
```

## 3. 硬件驱动层
- GPS芯片驱动 (UART/SPI通信)
- Wi-Fi芯片驱动 (扫描热点)
- 蜂窝基站驱动 (基站信息)

## 完整调用链
JavaScript API → 浏览器引擎(C++) → 操作系统API → 硬件驱动 → 物理硬件
