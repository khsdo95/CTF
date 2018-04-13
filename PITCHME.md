## Vulnerability and Exploitation 
- Hongsik Kim
- VOM (VIM Onion Messenger)

---

## New Features
1. Image File Cache
2. /r, /rpl Command

---

## Vulnerabilities

+++
@title[Code]

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

@[1](Python from..import statement)
@[3-4](bbb)
@[4]

---

# Demo


