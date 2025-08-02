import dns.resolver

dns_record ={}

website = input("enter a website name:")

a_record = dns.resolver.resolve(website, 'A')


for ipval in a_record:
    dns_record['A_Record_IP']=ipval.to_text()


mx_record_list = []

mx_record=dns.resolver.resolve(website, 'MX')

for server in mx_record:
    mx_record_list.append(server)

for i, element in  enumerate(mx_record_list):
    dns_record['MX_Record', i+1] = element


for key, value in dns_record.items():
    print(f"{key}={value}")