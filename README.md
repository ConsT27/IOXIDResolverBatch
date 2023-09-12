# IOXIDResolverBatch
IOXID Scan in Batch. IOXID批量扫描，帮助在内网快速发现多网卡机器

IOXIDResolverBatch.py updated from AirBus Security https://github.com/mubix/IOXIDResolver

## Example Run

```
python IOXIDResolverBatch.py -t 10.1.1.1
python IOXIDResolverBatch.py -t 10.10.11.0/24  (支持CIDR）
python IOXIDResolverBatch.py -f ip.txt (读取文件里的ip从而扫描IOXID）
```
