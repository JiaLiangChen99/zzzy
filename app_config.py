from view.home import index,new, article, \
    expert, equipment, literature
from view.analyse_sys.system_home_page import home_data_dash

from view.analyse_sys import analyse_system_app
from view import login


class AppInitConfig:

    PASS_URL = {
        '/login' : login.login_ui,
        '/':index.index_page,
        '/home':index.index_page, #首页
        '/home/about' : None, #关于
        '/home/about/new' : new.home_new_UI, #新闻
        '/home/about/new/article': article.article_UI,  # 新闻
        '/home/about/people' : expert.expert_UI, #相关领导
        '/home/about/partners' : None, #合作伙伴
        '/home/about/cite' : None, #如何引用
        '/home/about/equipment': equipment.equipment_ui,  # 设备展示
        '/home/analyse/seedresource' : None, #种质资源
        '/home/analyse/Phenotyping' : None, #表型分析
        '/home/analyse/Genotyping' : None, #基因型分析
        '/home/analyse/MultiOmicAnalysis' : None, #多组学分析
        '/home/publice/literature' : literature.literature_UI , #文献下载
        '/home/publice/seedtrade' : None, #种质交易
        '/home/publice/seedinfo' : None, #种质详情信息
        '/analysesystem' : analyse_system_app.system_app_main
    }


class AnalyseSystemConfig:
    # 顶端进度条需要忽略的监听目标
    exclude_props = [
        'side-menu.style',
        'fold-side-menu-icon.icon',
        'overview-fullscreen.isFullscreen'
    ]

    # 定义侧边菜单树状结构数据
    menuItems = [
                {
                'component': 'Item',
                'props': {
                    'key': f'主页',
                    'title': f'主页'
                }
            },
        {
            'component': 'SubMenu',
            'props': {
                'key': f'数据管理',
                'title': f'数据管理'
            },
            'children' : [
                {
                    'component': 'Item',
                    'props': {
                        'key': f'数据管理|团队管理',
                        'title': f'团队管理'
                    }
                },
                {
                    'component': 'Item',
                    'props': {
                        'key': f'数据管理|项目数据管理',
                        'title': f'项目数据管理'
                    }
                },
            ]
        },
        {
            'component': 'SubMenu',
            'props': {
                'key': f'基因型分析',
                'title': f'基因型分析'
            },
            'children': [
                {
                    'component': 'SubMenu',
                    'props': {
                        'key': f'基因型分析|位点管理',
                        'title': f'位点管理'
                    },
                    'children':[
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|位点管理|SNP位点管理',
                                'title': f'SNP位点管理'
                            }
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|位点管理|SNP Panel位点管理',
                                'title': f'SNP Panel位点管理'
                            }
                        }
                    ]
                },
                {
                    'component': 'SubMenu',
                    'props': {
                        'key': f'基因型分析|分析工具',
                        'title': f'分析工具'
                    },
                    'children' : [
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|分析工具|品种基因型比较',
                                'title': f'品种基因型比较'
                            }
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|分析工具|进化树',
                                'title': f'进化树'
                            }
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|分析工具|遗传距离',
                                'title': f'遗传距离'
                            }
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|分析工具|PCA分析',
                                'title': f'PCA分析'
                            }
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|分析工具|ADMIXTURE分析',
                                'title': f'ADMIXTURE分析'
                            }
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'基因型分析|分析工具|目标基因分析',
                                'title': f'目标基因分析'
                            }
                        },
                    ]
                },

            ]
        },
        {
            'component': 'SubMenu',
            'props': {
                'key': f'表型分析',
                'title': f'表型分析'
            },
            'children': [
                {
                    'component': 'Item',
                    'props': {
                        'key': f'表型分析|仪表盘',
                        'title': f'仪表盘'
                    },
                },
                {
                    'component': 'SubMenu',
                    'props': {
                        'key': f'表型分析|分析工具',
                        'title': f'分析工具'
                    },
                    'children': [
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'表型分析|分析工具|两两比对分析',
                                'title': f'两两比对分析'
                            }
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'表型分析|分析工具|单品种分析',
                                'title': f'单品种分析'
                            }
                        }
                    ]
                },

            ]
        },
        {
            'component': 'SubMenu',
            'props': {
                'key': f'系统后台',
                'title': f'系统后台'
            },
            'children': [
                {
                    'component': 'Item',
                    'props': {
                        'key': f'系统后台|文章管理',
                        'title': f'文章管理'
                    },
                },
                {
                    'component': 'Item',
                    'props': {
                        'key': f'系统后台|资源管理',
                        'title': f'资源管理'
                    }
                },

            ]
        }
        ]





