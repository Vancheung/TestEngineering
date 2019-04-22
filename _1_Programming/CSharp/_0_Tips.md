1、C#没有全局变量或全局函数，使用静态变量和静态函数实现

2、所有的C#类型都是从object类继承的，包括基本类型（int/float/string等）、用户自定义类型（class、struct、interface）
值类型——堆栈中分配，包括：除字符串外所有基本和内建类型、结构、枚举
引用类型：heap中创建，new创建，自动回收，包括：类、接口、集合类型（eg:数组）、字符串

3、使用一个对象作为属性时，在get时检测对象实例是否为null，为null则new一个新的实例。eg：
get
{
	if(day==null)
	{
		this .day = new Day();
	}
	return this.day;
}

4、readonly：间接或直接初始化时赋值，赋值后只能读取
const：声明时直接初始化

5、seal：不允许从它继承任何类

6、接口：只包含函数声明而在子类中实现的抽象基类
C#不能对类进行多重继承，只能通过接口实现

7、虚函数：父类使用virtual，子类使用override重写（只在子类中实现：父类加abstract关键字）。eg：
Class A
{
	Public virtual void doA()
	{
		//do something
	}
	Public abstract void doAA();
}
Class B
{
	Public override void doA()
	{
		//do something
	}
	Public override void doB()
	{
		//do something
	}
}

8、ref：按引用传递

9、out：输出参数

10、C#使用params数组传递可变数量的参数或数组，数组类型的参数必须放在函数最右边的参数

11、is：两个操作数是否相等或可互相转换，返回bool
as：两个操作数是否相等或可互相转换，是则返回已转换后的对象，否则返回null

12、delegate：保存函数的引用
