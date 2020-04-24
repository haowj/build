# coding:utf-8
__author__ = 'xcma'
from git import Repo
import logging
from appack.helper.misc import executionShell
from appack.models import Operatingtag
log = logging.getLogger(__name__)

class git_process:
    """
    git 操作

    """
    def __init__(self,project_path):
        self.project_path=project_path
        log.debug('project_path:{}'.format(project_path))
        self.repo = Repo(project_path)
        self.index = self.repo.index
        # 获取默认版本库 origin
        self.remote = self.repo.remote()
        self.git = self.repo.git

    def bare(self):
        # 版本库是否为空版本库
        return self.repo.bare
    def is_dirty(self):
        # 当前工作区是否干净
        return self.repo.is_dirty()

    def untracked_files(self):
        # 版本库中未跟踪的文件列表
        return self.repo.untracked_files

    def fetch_reset(self,branch=''):
        """
        git fetch --all
        git reset --hard origin/zjsuperd
        实现有问题
        :return: 
        """
        for remote in self.repo.remotes:
            remote.fetch()
        if branch:
            self.git.reset('--hard', 'origin/{}'.format(branch))
        else:
            self.git.reset('--hard')
    def clone(self):
        # 克隆版本库
        return self.repo.clone('clone_path')

    def archive(self,pathname):
        # 压缩版本库到 tar 文件
        with open(pathname, 'wb') as fp:
            self.repo.archive(fp)
    def create_head(self,branchname):
        # 新建分支
        return self.repo.create_head(branchname)

    def active_branch(self):
        # 查看当前分支
        try:
            res = self.repo.active_branch
            log.debug('当前分支：{}'.format(res))
            return res
        except Exception as e:
            log.error(e)

    def getTagList(self):
        """获取项目中所有tag,并排序"""
        self.init_project()
        tag_list = []
        tag_dict = {}
        a = self.repo.tags
        for i in a:
            tag = i.name
            try:
                si = int(tag.replace('.','').replace('-',''))
                tag_dict[si] = tag
            except:
                pass

        tag_int_list=list(tag_dict.keys())
        tag_int_list.sort()
        for i in tag_int_list:
            tag_list.append(tag_dict[i])

        log.debug('tag_list:{}'.format(tag_list))
        return list(reversed(tag_list))

    def add(self,filename='.'):
        return self.index.add([filename])

    def gitadd(self,filename='.'):
        return self.git.add(filename)

    def remove(self,filename='.'):
        return self.index.remove([filename])

    def commit(self,msg):
        log.debug('commit:{}'.format(msg))
        return self.index.commit(msg)

    def pull(self):
        res = self.remote.pull()
        # res = self.repo.git.pull('origin zjsuperd')
        log.debug('pull:{}'.format(res))
        # 从远程版本库拉取分支
        return res

    def push(self,origin=None):
        res = self.remote.push(origin)
        log.debug('push:{}'.format(res))
        # 推送本地分支到远程版本库
        return res

    def checkout(self,name):
        log.debug('checkout:{}'.format(name))
        res = self.repo.git.checkout(name)
        self.all_branches()
        self.active_branch()
        return res

    def reset_tag(self,tag):
        log.debug('开始切换版本,目标版本：{}'.format(tag))
        res = self.repo.git.reset('--hard',tag)
        log.debug('reset_tag_res:{}'.format(res))
        self.active_branch()

    def describe_tag(self):
        tagInfo = "git describe --always --tags `git rev-parse HEAD`"
        res = self.git.describe('--always','--tags')
        log.debug('当前tag为:{}'.format(res))
        self.git.rev_parse()
        return res

    def getLog(self,n='-1'):
        res = self.git.log(n)
        log.debug('更新内容：\n{}'.format(res))
        return res

    def init_project(self):
        try:
            log.debug('获取最新代码:开始')
            res = self.repo.git.checkout('.')
            log.debug('checkout:{}'.format(res))
            res = self.repo.git.clean('-df')
            log.debug('clean:{}'.format(res))
            self.pull()
            log.debug('获取最新代码:完成')
            self.getLog()
            self.active_branch()
        except Exception as e:
            log.error(e)

    def _init_directoy(self,branch):
        """
        初始化项目
        git fetch --all
        git reset --hard origin/zjsuperd
        :return:
        """
        try:
            log.debug('重置本地为远端git库:开始')
            try:
                cmd = ['git fetch --all','git reset --hard origin/{}'.format(branch),'git checkout . && git clean -xdf','git status']
                for c in cmd:
                    log.debug('初始化项目:{}'.format(c))
                    executionShell(c,self.project_path,50)
                # res = self.repo.git.checkout('.')
                # log.debug('checkout:{}'.format(res))
                # res = self.repo.git.clean('-df')
                # log.debug('clean:{}'.format(res))
                # self.pull()
                # log.debug('重置本地为远端git库:完成')
                # res = self.git.log('-1')
                # log.debug('最近一次更新：\n{}'.format(res))

            except Exception as e:
                log.error(e)
            self.change_branch(branch)
        except Exception as e:
            log.error(e)

    def rename(self,name):
        # 重命名远程分支
        return self.remote.rename(name)

    def all_branches(self):
        '获取所有分支'
        ab = self.repo.branches
        log.debug('所有分支：{}'.format(ab))
        return ab

    def cur_branch(self):
        head = self.repo.head
        log.debug('当前分支：{}'.format(head))
        return head

    def change_branch(self, branch):
        try:
            log.info('切换分支到【{}】：开始'.format(branch))
            self.all_branches()
            self.active_branch()
            res = self.git.checkout(branch)
            log.debug('切换分支：{},结果：{}'.format(branch, res))
            self.active_branch()
            log.info('切换分支到【{}】：结束'.format(branch))
        except Exception as e:
            log.error(e)

    def createTag(self,tag,msg,sw,path,branch,user=''):

        try:
            self._init_directoy(branch)
            log.debug('新增tag:{},msg:{}'.format(tag,msg))
            cbranch = self.active_branch()
            msg = '当前分支：{}，{}'.format(cbranch,msg)
            self.repo.create_tag(tag,message=msg)
            res = self.repo.remotes.origin.push(tag)
            log.debug('推送tag成功:{}'.format(res))
            Operatingtag.objects.update_or_create(defaults={'project_path':path,'comment':msg,'user':user},project_name=sw,tag=tag)
            return res
        except Exception as e:
            log.error(e)


    def delTag(self,tag,sw):
        cmd_r = 'git push origin :refs/tags/{}'.format(tag)
        cmd_l = 'git tag -d {}'.format(tag)
        rdata = []
        for cmd in [cmd_r,cmd_l]:
            data = executionShell(cmd,self.project_path)
            rdata.append(data)
        Operatingtag.objects.filter(project_name=sw,
                               tag=tag).update(status=0)

        return rdata

    # 基本语句
    # from git import Repo    # 导入repo模块
    # repoPath = r'F:\workprojects\xxx\xxx' # 本地git库路径
    # repo = Repo(repoPath)   # 获取一个库
    # print(repo.branches)    # 获取所有的分支
    # print(repo.untracked_files) # 获取所有未加入版本的文件
    # print(repo.active_branch)   # 当前活动分支
    # print(repo.head.reference)  # 当前活动分支
    # print(repo.remotes.origin)  # 获取一个运程库
    # origin = repo.remotes.origin
    # print(origin.exists())      # 判断一个远程库是否存在
    #
    # #  切换分支
    # from git import Repo
    # repoPath = r'F:\workprojects\xxx\xxx'
    # repo = Repo(repoPath)
    # master = repo.heads.master          # 获取master分支
    # curBranch = repo.head.reference     # 当前活动分支
    # if curBranch != master:
    #     # repo.head.reference = master    # 切换到master,方法一
    #     repo.heads.master.checkout()    # 切换到master,方法二
    #
    #
    # # 强制放弃本地修改（新增、删除文件）
    # # 用命令行的方式
    # #   下面的语句相当于，两条命令行：git checkout . && git clean -df
    # from git import Repo
    # repoPath = r'F:\workprojects\xxx\xxx'
    # repo = Repo(repoPath)
    # repo.git.checkout('.')
    # repo.git.clean('-df')
    # ensure master is checked out
    # repo.heads.master.checkout()
    # blast any changes there (only if it wasn't checked out)
    # repo.git.reset('--hard')
    # remove any extra non-tracked files (.pyc, etc)
    # repo.git.clean('-xdf')
    # pull in the changes from from the remote
    # repo.remotes.origin.pull()