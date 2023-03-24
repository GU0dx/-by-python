--创建数据库

create database bookshop

--建立基本表

	use bookshop


create table 库存信息(
	书号 nchar(10) PRIMARY KEY, 
	图书类别 nchar(20) not null,
	图书数量 int not null
)

	create table 图书信息(
	书号 nchar(10) foreign key references 库存信息(书号),
	图书名称 nchar(20) NOT NULL ,
	图书类别 nchar(20) NOT NULL ,
	图书出版社 nchar(20) NOT NULL,
	图书价格 float not null,
	图书页数 int not null
)

create table 顾客信息(
	顾客号 nchar(10) NOT NULL PRIMARY KEY,
	姓名 nchar(20) NOT NULL,
	性别 nchar(20) NOT NULL,
	年龄 int NOT NULL,
	电话号码 nchar(20) not null,
	)
	create table 供应商信息(
	供应商号 nchar(10) NOT NULL PRIMARY KEY,
	供应商名称 nchar(20) NOT NULL,
	电话号码 nchar(20) NOT NULL,
	供应商地址 nchar(40) not null 
)

create table 进货信息(
	进货单号 nchar(10) NOT NULL PRIMARY KEY,
	书号 nchar(10) not NULL,
	图书类别 nchar(20) not NULL,
	供应商号 nchar(10) foreign key references 供应商信息(供应商号),
	图书进货数量 int NOT NULL,
	进货日期 date default (getdate())
)


create table 销售信息(
	销售单号 nchar(10) NOT NULL PRIMARY KEY,
	书号 nchar(10) foreign key references 库存信息(书号),
	顾客号 nchar(10) foreign key references 顾客信息(顾客号),
	图书销售数量 int NOT NULL,
	销售日期 date default (getdate()),
	销售金额 float null default (0)
)


--添加数据

insert into 图书信息 values ('001','水浒传','中国古代小说','新华出版社',45.2,540)
insert into 图书信息 values ('002','战争与和平','外国小说','外国出版社',30.0,440)
insert into 图书信息 values ('003','三国演义','中国古代小说','新华出版社',45.5,540)
insert into 图书信息 values ('004','朝花夕拾','中国近代散文','新华出版社',30.1,540)
select * from 图书信息


insert into 顾客信息 values 
('1','王壮','男',30,'1258468720'),
('2','张力','男',35,'1845846872'),
('3','马超','男',20,'5896668720'),
('4','小红','女',18,'1598468720')
select * from 顾客信息
insert into 顾客信息 values 
('6','王小壮','男',30,'1258468720')


insert into 供应商信息 values 
('01','好再来','5265655','中南大学'),
('02','德利','5265655','中南大学'),
('03','华夏好书','5265655','中南大学'),
('04','武功秘籍','5265655','中南大学')
select * from 供应商信息

delete 供应商信息 where 供应商号='hjgh'
insert into 进货信息 (进货单号,书号,图书类别,供应商号,图书进货数量)values('a1','005','中国散文','01',20)
insert into 进货信息 (进货单号,书号,图书类别,供应商号,图书进货数量)values('a2','002','外国小说','01',20)
insert into 进货信息 (进货单号,书号,图书类别,供应商号,图书进货数量)values('a3','005','中国散文','01',20)
insert into 进货信息 (进货单号,书号,图书类别,供应商号,图书进货数量)values('a4','001','中国古代小说','01',2) 
insert into 进货信息 (进货单号,书号,图书类别,供应商号,图书进货数量)values('a5','005','中国散文','02',20) 
select * from 进货信息

 
select * from 销售信息 
insert into 库存信息 values ('001','中国古代小说',10)
insert into 库存信息 values ('002','外国小说',20)
insert into 库存信息 values ('003','中国古代小说',20)
insert into 库存信息 values ('004','中国近代散文',20)
select * from 库存信息

delete 库存信息 where 书号='003'


-- 存储过程设置

--1. 创建存储过程查询某段时间内各种图书的进货和销售情况；
create procedure 进售信息
	@date1 date,
	@date2 date	
	AS
	select * from 进货信息 where 进货信息.进货日期>=@date1 and 进货信息.进货日期<=@date2
	select * from 销售信息 where 销售日期>=@date1 and 销售日期<=@date2
	go
	
	exec 进售信息 '2021-12-22','2021-12-23'
	drop procedure jx_list
	

-- 创建视图

--1. 创建视图查询各类图书的库存总数；

create view zl_numb 
as 
 select 图书类别,sum(图书数量) as 种类数量 from 库存信息 group by 图书类别
 go 

 select * from zl_numb
 
 
 --触发器
 
--1. 创建触发器当图书入库时自动修改相应图书的总量和存放仓库中该图书的数量；  
  -- 进货入库
	CREATE TRIGGER 库存增加 on 进货信息 for insert AS
	declare @num int
	declare @bnum nchar(10)
	declare @f  int
	declare @kinds nchar(20)
	select @num=图书进货数量,@bnum=书号,@kinds=图书类别 from inserted
	select @f=COUNT(@bnum)from 库存信息 where 书号=@bnum
	if @f>0
	begin
	update 库存信息 set 图书数量=图书数量+@num where 书号=@bnum
	end
	if @f<=0
	begin
		insert into 库存信息 values (@bnum,@kinds,@num)
	end
	go
	
	drop trigger 库存增加
--销售出库
	CREATE TRIGGER 库存减少 on 销售信息 for insert AS
		declare @num int
		declare @bnum nchar(10)
		declare @num1 int
		select @num=图书销售数量,@bnum=书号 from inserted
		select @num1=图书数量 from 库存信息 where @bnum=书号
		if @num1 <= @num
			begin
			if @num1=@num
			begin
			delete 库存信息 where 书号=@bnum
			end
			else
			begin
			print '销售失败，图书数量不够！'
			Rollback TRANSACTION
			end
			end
		else
			begin
			update 库存信息 set 图书数量=图书数量-@num where 书号=@bnum
			end
		go


-- 自动填入金钱数量

    create trigger 结账金额 on 销售信息 for insert as 
    declare @图书价格 float
    declare @销售数量 int 
    declare @销售单号 nchar(10)
    declare @书号 nchar(10)
    select @销售数量=图书销售数量,@销售单号=销售单号,@书号=书号 from inserted
    select @图书价格=图书价格 from 图书信息 where @书号=书号
    update 销售信息 set 销售金额=@图书价格*@销售数量 where @销售单号=销售单号
    go
    
	
	--对顾客性别进行约束
	create trigger 性别约束 on 顾客信息 for insert 
	as 
	declare @性别 nchar(20)
	declare @年龄 int
	select @性别=性别,@年龄= 年龄 from inserted
	if @性别!='男' and @性别!='女'
	begin
	print '性别格式错误！'
    Rollback TRANSACTION
	end
	if @年龄 not between 10 and 150
	begin
	print '年龄超出范围，必须在-150岁之间！'
    Rollback TRANSACTION
    end
	go
	
--设置完整性约束
--设置销售金额默认值是
alter table 销售信息 add default(0) for 销售金额
--设置级联删除更新，当库存信息中书号改变，图书信息中的学号也改变，当库存信息中数据删除时，图书中的数据也级联删除
alter table 图书信息 add constraint 库存删除 foreign key(书号) references 库存信息(书号) on delete CASCADE on update cascade
--设置库存信息和销售信息级联更新
alter table 销售信息 add constraint 销售更新 foreign key(书号) references 库存信息(书号) on update cascade 
--进货信息与库存信息之间级联删除更新
alter table 进货信息 add constraint 进货删除 foreign key(书号) references 库存信息(书号) on delete CASCADE on update cascade
--进货信息和供应商信息设置级联删除更新，使数据保持一致
alter table 进货信息 add constraint 供应商删除 foreign key(供应商号) references 供应商信息(供应商号) on delete CASCADE on update cascade
--销售信息与顾客信息建立级联删除，并在顾客号上，建立级联更新，以便数据更改。
alter table 销售信息 add constraint 顾客删除 foreign key(顾客号) references 顾客信息(顾客号) on delete CASCADE on update cascade

