import pymssql   
serverName = '127.0.0.1'    #目的主机ip地址
userName = '123'        #SQL Server身份账号
passWord = '123'        #SQL Server身份密码
dbName = 'bookshop'        #对应数据库名称
connect = pymssql.connect(serverName,userName, passWord,dbName,port='1433') #SQL Server身份验证建立连接
if connect:
        print("连接成功!")



class database(object):
    """数据库操作对象"""

    def __init__(self, url, username, password, databaseName, port, charset):
        self.url = url
        self.username = username
        self.password = password
        self.databaseName = databaseName
        self.port = port
        self.charset = charset
        self.connect = self.sql_server_conn()
        self.cursor = self.connect.cursor()

    def sql_server_conn(self):
        connect = pymssql.connect(self.url, self.username, self.password, self.databaseName, port=self.port,
                                  charset=self.charset)  # 服务器名,账户,密码,数据库名
        if connect:
            print(u"Success!!")
        return connect

    # 查看表的所有字段，
    # @table_name :表名
    def get_column_name(self, table_name):
        self.cursor.execute("select top 1 * from " + table_name)  # 执行sql语句
        data_dict = []
        for field in self.cursor.description:
            data_dict.append(field[0])
        print(data_dict)
        return data_dict

    # 得到数据库所有的表名
    def get_table_name(self):
        sql = "SELECT NAME FROM SYSOBJECTS WHERE XTYPE='U' ORDER BY NAME"
        self.cursor.execute(sql)  # 返回执行成功的结果条数
        rows = self.cursor.fetchall()
        for d in rows:
            for k in d:
                print(k)

    # 执行sql语句，增删改查
    # @sql:sql语句
    def execute_sql(self, sql):
        try:
            s1 = ''
            sql = sql.lower()
            if 'insert' in sql or 'delete' in sql or 'update' in sql:
                self.cursor.execute(sql)
                self.connect.commit()
                return
            elif 'select' in sql:
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                print("进货单号\t书号\t\t图书类型\t\t供应商号\t图书进货数量\t进货日期")
                for k in rows:
                    for k1 in k:
                        s1 += (str(k1).strip(' ')) + "\t\t"
                    s1 += '\n'
                if s1 == '':
                    print("无")
                print(s1)

        except :
            print("\033[1;31m 输入sql语句错误！自动返回菜单！\033[0m")

    def InGoods(self):
        # 先确定进货单号，再进货
        sql = 'select 进货单号 from 进货信息'
        s=''
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for k in rows:
            for k1 in k:
                s += (str(k1).strip(' ')) + " "
        print("已有进货单号：")
        if s == '':
            print("无")
        print(s)
        num = input("请输入进货单号:")
        bnum=input("请输入书号:")
        kinds = input("请输入图书类型:")
        inshopnum=input("请输入供应商号:")
        snum=input("请输入图书进货数量:")
        sql = "insert into 进货信息(进货单号,书号,图书类别,供应商号,图书进货数量) values ('" + num + "','" + bnum+ "','" + kinds+"','" + inshopnum + "',"+ snum+" )"
        self.execute_sql(sql)

    def sale(self):
        chose=input("你是要查看，还是添加? C/A")
        s = ''
        if chose == 'A' or chose == 'a':
            sql = 'select 书号 from 图书信息'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for k in rows:
                for k1 in k:
                    s += (str(k1).strip(' ')) + " "
            print("已上架书号：")
            if s=='':
                print("无")
            print(s)
            sql = 'select 书号 from 库存信息'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for k in rows:
                for k1 in k:
                    s += (str(k1).strip(' ')) + " "
            print("库存内书号：")
            if s == '':
                print("无")
            print(s)
            num = input("请输入要上架书号:")
            bname = input("请输入图书名:")
            kinds = input("请输入图书类别:")
            cbs = input("请输入图书出版社:")
            price = input("请输入图书价格:")
            ynum = input("请输入图书页数:")
            sql = "insert into 图书信息 values ('" + num + "','" + bname + "','" + kinds + "','" + cbs + "'," + price + "," + ynum + ")"
            print("正在上架...")
            if self.execute_sql(sql):
                print("上架成功")
        if chose == 'c' or chose == 'C':
            s1 = ''
            bnum = input("请输入书号:")
            sql = "select * from 图书信息 where 书号= '" + bnum + "'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            print("书号\t图书名称\t 图书类别\t图书出版社\t图书价格\t图书页数")
            for k in rows:
                for k1 in k:
                    s1 += (str(k1).strip(' ')) + "\t"
                s1 += '\n'
            if s1 == '':
                print("无此图书")
            print(s1)

    def InShoper(self):
        chose=input("你是要查看，还是添加? C/A:")
        sql = 'select 供应商号 from 供应商信息'
        s = ''
        if chose=='A' or chose=='a':
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for k in rows:
                for k1 in k:
                    s += (str(k1).strip(' ')) + " "
            print("已有供应商号：")
            if s == '':
                print("无")
            print(s)
            num = input("请输入供应商号:")
            name = input("请输入供应商名称:")
            tel = input("请输入供应商电话：")
            add = input("请输入供应商地址：")
            # sql=('insert into 供应商信息 values (%s,%s,%s,%s)'%(num,name,tel,add))
            sql = "insert into 供应商信息 values ('" + num + "','" + name + "','" + tel + "','" + add + "')"
            con.execute_sql(sql)
            chose='C'
        elif chose=='c' or chose=='C':
            s1 = ''
            self.cursor.execute('select * from 供应商信息')
            rows = self.cursor.fetchall()
            print('现有供应商如下：')
            print("供应商号\t供应商名称\t供应商电话\t供应商地址")
            for k in rows:
                for k1 in k:
                    s1 += (str(k1).strip(' ')) + "\t\t"
                s1 += '\n'
            if s1 == '':
                print("无")
            print(s1)
        else:
            print("输入错误！")
    def Customer(self):
        chose = input("你是要查看，还是添加? C/A:")
        sql = 'select 顾客号 from 顾客信息'
        s = ''
        if chose == 'A' or chose == 'a':
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for k in rows:
                for k1 in k:
                    s += (str(k1).strip(' ')) + " "
            print("已有顾客号：")
            if s == '':
                print("无")
            print(s)
            num = input("请输入顾客号:")
            name = input("请输入顾客姓名:")
            tel = input("请输入顾客电话：")
            age = input("请输入顾客年龄: ")
            sex = input("请输入顾客性别：")
            # sql=('insert into 供应商信息 values (%s,%s,%s,%s)'%(num,name,tel,add))
            sql = "insert into 顾客信息 values ('" + num + "','" + name + "','" + sex + "'," + age + ",'" + tel + "')"
            # print(sql)
            con.execute_sql(sql)
        if chose == 'c' or chose == 'C':
            s1 = ''
            gknum=input("请输入顾客号:")
            sql="select * from 顾客信息 where 顾客号= '"+gknum+"'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            print("顾客号\t顾客姓名\t顾客性别\t顾客年龄\t\t顾客电话")
            for k in rows:
                for k1 in k:
                    s1 += (str(k1).strip(' ')) + "\t\t"
                s1 += '\n'
            if s1 == '':
                print("无")
            print(s1)

    def CheckOut(self):
        sql = 'select 销售单号 from 销售信息'
        s = ''
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for k in rows:
            for k1 in k:
                s += (str(k1).strip(' ')) + " "
        print("已用销售单号：")
        if s == '':
            print("无")
        print(s)
        num = input("请输入销售单号:")
        name = input("请输入书号:")
        uname = input("请输入顾客号：")
        add = input("请输入销售图书数量：")
        # sql=('insert into 供应商信息 values (%s,%s,%s,%s)'%(num,name,tel,add))
        sql = "insert into 销售信息(销售单号,书号,顾客号,图书销售数量) values ('" + num + "','" + name + "','" + uname + "'," + add + ")"
        # print(sql)
        con.execute_sql(sql)
        s1 = ''
        try:
            sql="select 销售金额 from 销售信息 where 销售单号= '"+num+"'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
        except:
            print("sql语句错误！")
        for k in rows:
            for k1 in k:
                s1=(str(k1).strip(' '))
        print("应付金额 ："+s1)
    def record(self):
        chose= input("查看哪个记录？1.进货记录 2.销售记录:")
        if chose=='1':
            s1=''
            sql = 'select * from 进货信息'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            print("进货单号\t书号\t\t图书类别\t\t供应商号\t图书进货数量\t进货日期")
            for k in rows:
                for k1 in k:
                    s1 += (str(k1).strip(' ')) + "\t\t"
                s1 += '\n'
            if s1 == '':
                print("无")
            print(s1)
        if chose=='2':
            s1 = ''
            sql = 'select * from 销售信息'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            print("销售单号\t书号\t 顾客号\t图书销售数\t销售日期\t\t  销售金额")
            for k in rows:
                for k1 in k:
                    s1 += (str(k1).strip(' ')) + "\t\t"
                s1 += '\n'
            if s1 == '':
                print("无")
            print(s1)
        else:
            print("输入错误！")

    def Stock(self):
        s1 = ''
        sql = 'select * from 库存信息'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        print("书号\t\t图书类别 \t库存量")
        for k in rows:
            for k1 in k:
                s1 += (str(k1).strip(' ')) + "\t\t"
            s1 += '\n'
        if s1 == '':
            print("无")
        print(s1)


    def menu(self):
        print("欢迎来到书店！")
        while True:
            print("服务菜单如下：")
            print('1.进货')
            print('2.查看/上架图书')
            print('3.查看/新增供应商')
            print('4.查看/新增会员')
            print('5.结账')
            print('6.查看进货和销售记录')
            print('7.查看库存容量')
            print('0.离开')
            key = input("请选择需要的服务：")
            if key == '1':
                con.InGoods()
                input("按回车继续")

            elif key == '2':
                con.sale()
                input("按回车继续")

            elif key == '3':
                con.InShoper()
                input("按回车继续")

            elif key == '4':
                con.Customer()
                input("按回车继续")

            elif key == '5':
                con.CheckOut()
                input("按回车继续")

            elif key == '6':
                con.record()
                input("按回车继续")

            elif key == '7':
                con.Stock()
                input("按回车继续")

            elif key == '0':
                exit_course = input('确定退出吗？（y/n）:')
                if exit_course == 'y' or exit_course=='Y':
                    exit()
                else:
                    pass
            else:
                print("请输入正确的数值！")

    # 关闭游标，连接
    def close(self):
        self.cursor.close()  # 关闭游标
        self.connect.close()


if __name__ == '__main__':
    con = database('127.0.0.1', '123', '123', 'bookshop', '1433', 'utf8')
    con.menu()

