一个 todo list 后端上有两种状态
- 未完成
- 已完成

本质上是两个数组

每次鼠标的点击都会将未完成的移动到已完成里



还有一个鼠标 event 事件 点击一个button 热区 然后就会往未完成里面 push 一个新对象

然后这个对象此时用户会进行编辑有 focus 和 no focus 两种状态 focus 意味着在编辑态里


现在的逻辑是有一个 input 组件 我需要在 input 中输入然后点击 add 才可以 push 一个 new task
但是这并不合理，我希望的 ux 是 add 直接 render 一个 空 task 然后这个task 可以被编辑

没考虑到的：渲染