import time  
import requests

def fetch_data(url):  
    print(f"開始下載 {url}...")  
    response = requests.get(url)  
    print(f"完成下載 {url}，資料長度: {len(response.text)}")  
    return response.text

def main():  
    start_time = time.time()  
    urls = [  
        "[https://httpbin.org/delay/2](https://httpbin.org/delay/2)",  
        "[https://httpbin.org/delay/1](https://httpbin.org/delay/1)",  
        "[https://httpbin.org/delay/2](https://httpbin.org/delay/2)"  
    ]  
      
    results = []  
    for url in urls:  
        results.append(fetch_data(url))  
          
    end_time = time.time()  
    print(f"\\n所有下載完成！總共耗時: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":  
    main()