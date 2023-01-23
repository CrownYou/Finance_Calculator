import time
import sympy as sp
parameter_dic = {'1': '期数', '2': '每期利率', '3': '每期现金流', '4': '现值', '5': '终值'}
print('金融计算器，开发者：扬州大学 顾浪屿')

while True:
    def numerize(st: str):
        if ',' in st:
            lst = st.split(',')
        elif '，' in st:
            lst = st.split('，')
        else:
            lst = [st]
        res = []
        for i in lst:
            if '*' in i:
                a = eval(i.split('*')[0])
                for j in range(eval(i.split('*')[1])):
                    res.append(a)
            else:
                res.append(eval(i))
        return res


    def check_eval(st):
        while True:
            try:
                res = eval(st)
            except Exception:
                st = input('输入不对哦~请重新输入:')
            else:
                return res


    def update_data_dic(key: str):
        if key != '2' and key != '3':
            data_dic[parameter_dic[key]] = check_eval(input('请输入{}的值：'.format(parameter_dic[key])))
        if key == '2':
            data_dic[parameter_dic[key]] = check_eval(input('请输入{}的值(%)：'.format(parameter_dic[key])).strip().strip('%'))/100
        if key == '3':
            while True:
                print('\n===现金收付类型如何？===\n'
                      '1.每期现金流相等\n'
                      '2.每期现金流按一定比例变化\n'
                      '3.每期现金流不规律变化')
                flag = input('请选择现每期现金流的变化情况：')
                if flag == '2':
                    if '每期现金流' in data_dic:
                        del data_dic['每期现金流']
                    data_dic['首次现金流'] = check_eval(input(('请输入首次现金流的值：')))
                    data_dic['每期现金流变化率'] = check_eval(input('请输入每期增加或减少的比例(%)：').strip().strip('%'))/100
                    break

                else:
                    if '首次现金流' in data_dic:
                        del data_dic['首次现金流']
                    if '每期现金流变化率' in data_dic:
                        del data_dic['每期现金流变化率']
                    if flag == '1':
                        data_dic['每期现金流'] = check_eval(input(('请输入{}的值：'.format('每期现金流'))))
                        break
                    if flag == '3':
                        pmt = input('请输入每期现金流的值，使用逗号分隔（可使用\'*\'号表示几次重复的现金流，如100*2，150*3):')
                        data_dic['每期现金流'] = numerize(pmt)
                        break
                    else:
                        print('输入不对哦，请重新输入')
        print(data_dic)


    def parameter_table():  # 返回已经被赋值过的参数的参数表，和未被赋值的键
        for key in table.keys():
            dic = parameter_dic.copy()
            del dic[key]
            st = str(dic).lstrip('{').rstrip('}').replace('\': \'', '.').replace('\'', '').replace(',', '')
            return ['\n==========参数修改==========\n' + st + '\n', key]


    def change_data_dic():
        while True:
            print(parameter_table()[0])
            key = input('请输入想要修改的对象:')
            if key in parameter_dic and key != parameter_table()[1]:
                update_data_dic(key)
                break
            else:
                print('输入不对哦，请重新输入')

    # 以下是程序主要部分
    print('\n请注意现金流正负哦！\n'
          '流入为正，流出为负\n'
          '百分号可省略，直接书写\'%\'前的数字即可\n')
    time.sleep(0.5)
    data_dic = {}
    while True:
        print('=====每期现金流流动时点=====\n'
              '1.期初 2.期末')
        mode_dic = {'1': '期初', '2': '期末'}
        mode = input('请输入每期现金流流动时点：')
        if mode in mode_dic:
            data_dic['每期现金流流动时点'] = mode_dic[mode]
            print(data_dic)
            break
        else:
            print('输入不对哦，请重新输入\n')

    table = {'1': '期数', '2': '每期利率', '3': '每期现金流', '4': '现值', '5': '终值'}
    for i in range(1, 5):
        while True:
            print('\n==========参数表==========')
            print(str(table).lstrip('{').rstrip('}').replace('\': \'', '.').replace('\'', '').replace(',', ''))
            key = input('请输入想要赋值的对象({}/4):'.format(i))
            if key in table:
                update_data_dic(key)
                del table[key]
                break
            else:
                print('\n请在参数表中选择需要赋值的参数，如需修改请在赋值完成后再进行哦')
                time.sleep(0.5)

    while True:
        if '每期现金流' in data_dic and type(data_dic['每期现金流']) == list and '期数' in data_dic and len(data_dic['每期现金流']) != data_dic['期数']:
            print('\n现金流数量:{} 与 期数:{}不一致哦，请修改一下'.format(len(data_dic['每期现金流']), data_dic['期数']), end='')
            change_data_dic()
            continue
        if '每期现金流' in data_dic and type(data_dic['每期现金流']) == list and '期数' not in data_dic:
            data_dic['期数'] = len(data_dic['每期现金流'])
            print('\n===信息出现多余===')
            print(f'''1.期数:{data_dic['期数']}; 2.每期利率:{data_dic['每期利率']}; 3.每期现金流:{data_dic['每期现金流']}; 4.现值:{data_dic['现值']}; 5.终值:{data_dic['终值']}''')
            key = input('请输入你需要求解的对象：')
            data_dic.pop(parameter_dic[key])
            continue
        else:
            print('\n参数输入完毕，还有需要修改的嘛？')
            print(data_dic)
            flag = input('需要修改请按\'Y\'，不需要修改请按其他任意键:')
            if flag == 'Y':
                change_data_dic()
                continue
            else:
                print('\n赋值完毕，即将求解:{}'.format(parameter_dic[parameter_table()[1]]))
                break

    # 以下为数据处理部分
    # {'每期现金流流动时点': '期末', '期数': 2, '每期利率': 0.02, '每期现金流': [180, 180], '现值': 4}
    # {'每期现金流流动时点': '期末', '期数': 2, '每期利率': 0.02, '现值': 4, '首次现金流': 12, '每期现金流变化率': 0.12}
    # {'每期现金流流动时点': '期末', '期数': 2, '每期利率': 0.02, '现值': 4, '每期现金流': 1}


    def wash_ans(ans):  # 将结果中的虚根洗掉，并返回相应的结果
        res = []
        for i in ans:
            i = str(i.evalf(99))
            if 'I' not in str(i):
                ind_of_dot = i.index('.')
                i = i[:ind_of_dot + 9]
                res.append(float(i))
        if res:
            print(f'{parameter_dic[parameter_table()[1]]}：{res}')
        else:
            print('无解')


    code = '''
Sn = n * PMT / (1 + r) if g == r else PMT * (1 - ((1 + g) / (1 + r)) ** n) / (r - g)
Sn = Sn if data_dic['每期现金流流动时点'] == '期末' else Sn * (1 + r)
fx = PV + Sn + FV / ((1 + r) ** n)
            '''

    # 这里是求每期现金流的部分
    if parameter_dic[parameter_table()[1]] == '每期现金流':
        while True:
            print('===想要求解什么样的现金流？===\n'
                  '1.每期现金流相等\n'
                  '2.每期现金流按一定比例变化')
            flag = input('请选择现每期现金流的变化情况：')
            if flag == '1':
                PMT = sp.symbols('PMT')
                g = 0
                n = data_dic['期数']
                r = data_dic['每期利率']
                PV = data_dic['现值']
                FV = data_dic['终值']
                exec(code)
                raw_ans = sp.solve(fx, PMT)
                res = []
                for i in raw_ans:
                    if 'I' not in str(i):
                        res.append(i)
                if res:
                    print(f'每期现金流：{res}')
                else:
                    print('无解')
                break
            if flag == '2':
                g = eval(input('请输入每期现金流的变化率(%)：').strip().strip('%')) / 100
                PMT = sp.symbols('PMT')
                n = data_dic['期数']
                r = data_dic['每期利率']
                PV = data_dic['现值']
                FV = data_dic['终值']
                exec(code)
                raw_ans = sp.solve(fx, PMT)
                res = []
                for i in raw_ans:
                    if 'I' not in str(i):
                        res.append(i)
                if res:
                    print(f'首次现金流：{res}')
                else:
                    print('无解')
                break

            else:
                print('输入不对哦，请重新输入\n')

    else:  # 求解 除了每期现金流之外的值
        # 需要先对不规则变化的现金流进行处理，处理成PMT_i = xxx
        if '每期现金流' in data_dic and type(data_dic['每期现金流']) == list:
            for i in range(len(data_dic['每期现金流'])):
                assign = f'''
PMT_{i} = data_dic['每期现金流'][i]
                '''
                exec(assign)  # 将所有现金流赋值给PMT_i

            code2 = f'''
for i in range(len(data_dic['每期现金流'])):
    Sn += PMT_{i} / ((1 + r) ** {i})    
Sn = Sn if data_dic['每期现金流流动时点'] == '期末' else Sn * (1 + r)
fx = PV + Sn + FV / ((1 + r) ** n)
            '''

            Sn = 0
            # 数据清洗完毕，接下来可以进行处理
            if parameter_dic[parameter_table()[1]] == '期数':
                # 由于不规则现金流的个数已经暗含了期数，且计算前已经报错过，这里无需处理
                pass
            if parameter_dic[parameter_table()[1]] == '每期利率':
                r = sp.symbols('r')
                n = data_dic['期数']
                PV = data_dic['现值']
                FV = data_dic['终值']
                exec(code2)
                raw_ans = sp.solve(fx, r)
                wash_ans(raw_ans)

            if parameter_dic[parameter_table()[1]] == '现值':
                PV = sp.symbols('PV')
                n = data_dic['期数']
                r = data_dic['每期利率']
                FV = data_dic['终值']
                exec(code2)
                raw_ans = sp.solve(fx, PV)
                wash_ans(raw_ans)

            if parameter_dic[parameter_table()[1]] == '终值':
                FV = sp.symbols('FV')
                n = data_dic['期数']
                r = data_dic['每期利率']
                PV = data_dic['现值']
                exec(code2)
                raw_ans = sp.solve(fx, FV)
                wash_ans(raw_ans)

            print('注意：在每期现金流不等的情况下，结果精度会变低')

        # 如果每期现金流是规则的（每一期都一样，每一期按一定比例变化）
        # 则将每一期都一样处理成为每一期变化率为0
        else:
            if '每期现金流' in data_dic:
                data_dic['每期现金流变化率'] = data_dic.get('每期现金流变化率', 0)
                data_dic['首次现金流'] = data_dic.get('首次现金流', data_dic['每期现金流'])
                data_dic.pop('每期现金流')

            # 数据清洗完毕，接下来可以进行处理
            if parameter_dic[parameter_table()[1]] == '期数':
                n = sp.symbols('n')
                PMT = data_dic['首次现金流']
                g = data_dic['每期现金流变化率']
                r = data_dic['每期利率']
                PV = data_dic['现值']
                FV = data_dic['终值']
                exec(code)
                raw_ans = sp.solve(fx, n)
                wash_ans(raw_ans)

            if parameter_dic[parameter_table()[1]] == '每期利率':
                r = sp.symbols('r')
                n = data_dic['期数']
                PMT = data_dic['首次现金流']
                g = data_dic['每期现金流变化率']
                PV = data_dic['现值']
                FV = data_dic['终值']
                exec(code)
                raw_ans = sp.solve(fx, r)
                wash_ans(raw_ans)

            if parameter_dic[parameter_table()[1]] == '现值':
                PV = sp.symbols('PV')
                n = data_dic['期数']
                PMT = data_dic['首次现金流']
                g = data_dic['每期现金流变化率']
                r = data_dic['每期利率']
                FV = data_dic['终值']
                exec(code)
                raw_ans = sp.solve(fx, PV)
                wash_ans(raw_ans)

            if parameter_dic[parameter_table()[1]] == '终值':
                FV = sp.symbols('FV')
                n = data_dic['期数']
                PMT = data_dic['首次现金流']
                g = data_dic['每期现金流变化率']
                r = data_dic['每期利率']
                PV = data_dic['现值']
                exec(code)
                raw_ans = sp.solve(fx, FV)
                wash_ans(raw_ans)

    # 结尾部分：询问是否需要再次计算
    again = input('\n需要再次计算请按\'Y\'或\'y\'，其他任意键退出程序：')
    if again != 'Y' and again != 'y':
        break
