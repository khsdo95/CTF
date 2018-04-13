## Vulnerability and Exploitation 
- Hongsik Kim (w/ VOM)

---

## New Features
1. Image File Cache
2. /r, /rpl Command

---

## Vulnerabilities

+++

### Utils/Cache.cc

```C++
#include "Cache.hh"

namespace Cache {
    Cache::Cache() {
        count = 0;
    }
    Cache::~Cache() {
    }
    
    Element* Cache::find(string url) {
        for (auto it = data.begin(); it != data.end(); ++it) {
            if (!strcmp(url.c_str(), (*it).first.c_str()))
                return (*it).second;
        }
        return NULL;
    }


    void Cache::insert(string url, string sender, string path) {
        if (this->is_full())
            return;
        Element* elem = new Element(path, sender);
        data.push_back(make_pair(url, elem));
        count++;
    }

    Element* Cache::remove(string url) {
        auto elem = this->find(url);
        if (elem){
            for (auto it = data.begin(); it != data.end(); ++it) {
                if (!url.compare((*it).first)) {
                    it = data.erase(it);
                    return elem;
                }
            }
        }
        return elem;
    }

    void Cache::update(string url) {
        auto elem = this->remove(url);
        if (elem) {
            data.push_back(make_pair(url, elem));
        }
    }

    void Cache::pop() {
        auto it = data.begin();
        ++it;
        delete (*it).second;
        data.erase(it);
        count--;
    }

    Element::Element(string _path, string _sender) {
        path = _path;
        sender = _sender;
    }
    Element::~Element() {
    }
    
    string Element::GetPath() {
        return path;
    }

    string Element::GetSender() {
        return sender;
    }
}
```

@[10-16](Cache::find)
@[12](Using strcmp)
@[27-38](Cache::remove)
@[31](Using String::compare)


---

### poc.cc

```C++
using namespace std;

int main(){
    char buf[100] = "abcd\x00efg";
    string s1 = string(buf, 8);
    string s2 = string(buf);
    
    if (!strcmp(s1.c_str(), s2.c_str()))
        cout << "strcmp equal!!" << endl;

    if (!s1.compare(s2))
        cout << "compare equal!!" << endl;
}
```

@[9](Executed)

---

### OnionMessenger.cc

```C++
    void OnionMessenger::HandleAArt(Message::ImgLayer *msg) {                      
        auto sender = msg->GetSender();                                            
        auto url = msg->GetUrl();                                                  
        auto elem = image_cache->find(url);                                        
        string path;                                                               
        if (!elem){		// Cache Miss                                                              
            provider->PushChat(sender, "\n" + Features::DisplayAArt(url, path));
            if (image_cache->is_full()) {                                          
                image_cache->pop();                                                
            }                                                                      
            image_cache->insert(url, sender, path);                                
        } else {		// Cache Hit                                                               
            provider->PushChat(sender, "\n" + Features::Asciiart(elem->GetPath().c_str()));
            image_cache->update(url);                                              
        }                                                                          
        snprintf(recent_user, MAX_ID_LEN, "%s", sender.c_str());                   
        delete msg;                                                                
    }                                                
```

@[6-11](Cache Miss)
@[12-15](Cache Hit)

---
 
### Utils/Cache.cc

```C++
    void Cache::insert(string url, string sender, string path) {
        if (this->is_full())
            return;
        Element* elem = new Element(path, sender);
        data.push_back(make_pair(url, elem));
        count++;
    }

    void Cache::update(string url) {
        auto elem = this->remove(url);
        if (elem) {
            data.push_back(make_pair(url, elem));
        }
    }

    void Cache::pop() {
        auto it = data.begin();
        ++it;
        delete (*it).second;
        data.erase(it);
        count--;
    }

    Element::Element(string _path, string _sender) {
        path = _path;
        sender = _sender;
    }
    Element::~Element() {
    }
    
    string Element::GetPath() {
        return path;
    }

    string Element::GetSender() {
        return sender;
    }
}
```

@[8-13](Cache::update)
@[15-21](Cache::pop)

---

## Exploit Scenario

1. HandShake with target. |
2. Send a image packet. |
3. Send a image packet with `previous url + \"\x00BBBB\"`. It will trigger a bug. |
4. Send some image packets to trigger `Cache::pop`. It will delete a Element. |
5. Send a image packet to fill free area with setting path to our payload. |
6. Send a image packet with same url in step 2. It will trigger `Cache::Element::GetPath` with controlled element. |
7. We can exploit command injection with manipulated `path` |
8. Get a shell! |

---

# Demo


