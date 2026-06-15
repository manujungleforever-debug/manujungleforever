with open('scratch_3day.html','r',encoding='utf-8',errors='replace') as f:
    c = f.read()
print('Lines:', c.count('\n'))
print('Has body tag:', '<body' in c)
print('Has header:', '<header' in c)
print('Has in-hero:', 'in-hero' in c)
print('Has tour-layout:', 'tour-layout' in c)
print('Has </head>:', '</head>' in c)
# show first 300 chars after </head>
idx = c.find('</head>')
if idx > 0:
    print('After </head>:')
    print(c[idx:idx+400])
