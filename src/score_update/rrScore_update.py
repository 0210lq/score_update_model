import os
import pandas as pd
import src.global_setting.global_dic as glv
import sys
path = os.getenv('GLOBAL_TOOLSFUNC_new')
sys.path.append(path)
import global_tools as gt
from src.setup_logger.logger_setup import setup_logger
from datetime import date,datetime
inputpath_score=glv.get('input_score')
outputpath_score=glv.get('output_score')
inputpath_score_config=glv.get('score_mode')
import io
import contextlib
def capture_file_withdraw_output(func, *args, **kwargs):
    """捕获file_withdraw的输出并记录到日志"""
    logger = setup_logger('Score_update_sql')
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        result = func(*args, **kwargs)
        output = buf.getvalue()
        if output.strip():
            logger.info(output.strip())
    return result
class rrScore_update:
    def __init__(self,start_date,end_date,is_sql):
        self.is_sql=is_sql
        self.start_date=start_date
        self.end_date=end_date
        self.logger = setup_logger('Score_update')
        self.logger.info('\n' + '*'*50 + '\nSCORE UPDATE PROCESSING\n' + '*'*50)

    def raw_rr_time_checking(self,score_date, target_date):
        today = date.today()
        today=gt.strdate_transfer(today)
        if target_date>today:
            available_date2 = gt.last_weeks_lastday(target_date)
            if target_date > available_date2 and score_date != available_date2:
                self.logger.warning(f'请注意rr_score的最近更新日期是: {score_date} 上周最后一个工作日的日期是 {available_date2}, 已经自动用上上周的score进行更新！')
        
    def raw_rr_updating(self,mode_type):
        self.logger.info(f'\nProcessing RR score update for mode type: {mode_type}')
        df_config = pd.read_excel(inputpath_score_config)
        mode_name = df_config[df_config['score_mode'] == mode_type]['mode_name'].tolist()[0]
        outputpath_score3 = os.path.join(outputpath_score, mode_name)
        gt.folder_creator2(outputpath_score3)
        inputpath_score2 = os.path.join(inputpath_score, 'rr_score')
        outputpath_score2 = os.path.join(outputpath_score, 'rr_' + str(mode_type))
        try:
            inputlist = os.listdir(outputpath_score2)
        except:
            inputlist = []
        # if len(inputlist)==0:
        #     self.start_date='2024-01-01'
        #     self.logger.info('No existing files found, setting start date to 2024-01-01')
        rr_list = os.listdir(inputpath_score2)
        df_rr = pd.DataFrame()
        df_rr['rr'] = rr_list
        df_rr = df_rr[df_rr.rr.str.contains(str(mode_type))]
        df_rr['rr2'] = df_rr['rr'].apply(lambda x: str(x)[:8])
        df_rr = df_rr[df_rr['rr2'] == 'ThisWeek']
        df_rr.sort_values(by='rr')
        file_name = df_rr['rr'].tolist()[0]
        gt.folder_creator2(outputpath_score2)
        inputpath_score4 = os.path.join(inputpath_score2, 'W' + str(mode_type) + '_his_Ranking.xlsx')
        df_score = pd.read_excel(inputpath_score4, header=None)
        # 如果读出来是空表，则创建带列名的空 DataFrame；否则正常赋值
        if df_score.empty:
            df_score = pd.DataFrame(columns=['valuation_date', 'code'])
        else:
            df_score.columns = ['valuation_date', 'code']
        inputpath_score3 = os.path.join(inputpath_score2, file_name)
        df_score_this = pd.read_excel(inputpath_score3, header=None)
        df_score_this.columns = ['valuation_date', 'code']
        df_score=pd.concat([df_score,df_score_this])
        working_day_list = gt.working_days_list(self.start_date, self.end_date)
        if self.is_sql == True:
            inputpath_configsql = glv.get('config_sql')
            sm = gt.sqlSaving_main(inputpath_configsql, 'Score',delete=True)
        for date in working_day_list:
            self.logger.info(f'Processing date: {date}')
            available_date = gt.last_workday_calculate(date)
            available_date2=gt.intdate_transfer(available_date)
            # 先确保 valuation_date 是 datetime 类型
            df_score['valuation_date'] = pd.to_datetime(df_score['valuation_date'], errors='coerce')

            # 再转成字符串
            df_score['valuation_date'] = df_score['valuation_date'].dt.strftime('%Y-%m-%d')
            slice_df_score = df_score[df_score['valuation_date'] <= available_date]
            date3=slice_df_score['valuation_date'].unique().tolist()[-1]
            self.raw_rr_time_checking(date3, date)
            slice_df_score = df_score[df_score['valuation_date'] == date3]
            slice_df_score = gt.rank_score_processing(slice_df_score)
            slice_df_score['valuation_date'] = available_date
            slice_df_score2=slice_df_score.copy()
            slice_df_score2['score_name']=mode_name
            slice_df_score['score_name']='rr_'+str(mode_type)
            outputpath_saving = os.path.join(outputpath_score2, 'rr_' + str(available_date2) + '.csv')
            outputpath_saving2 = os.path.join(outputpath_score3, 'rr_' + str(available_date2) + '.csv')
            if len(slice_df_score) > 0 and len(slice_df_score2) > 0:
                slice_df_score.to_csv(outputpath_saving, index=False)
                slice_df_score2.to_csv(outputpath_saving2, index=False)
                self.logger.info(f'Successfully saved RR score data for date: {available_date2}')
                if self.is_sql==True:
                    now = datetime.now()
                    slice_df_score['update_time'] = now
                    slice_df_score2['update_time'] = now
                    capture_file_withdraw_output(sm.df_to_sql, slice_df_score,'score_name','rr_'+str(mode_type))
                    capture_file_withdraw_output(sm.df_to_sql, slice_df_score2,'score_name',mode_name)
    def raw_rr_updating2(self,mode_type):
        df_config = pd.read_excel(inputpath_score_config)
        print(df_config)
        mode_name = df_config[df_config['score_mode'] == mode_type]['mode_name'].tolist()[0]
        outputpath_score2 = os.path.join(outputpath_score, 'rr_' + str(mode_type))
        gt.folder_creator2(outputpath_score2)
        outputpath_score3 = os.path.join(outputpath_score, mode_name)
        gt.folder_creator2(outputpath_score3)
        self.logger.info(f'\nProcessing RR score update for mode type: {mode_type}')
        df_config = pd.read_excel(inputpath_score_config)
        inputpath_score2 = os.path.join(inputpath_score, 'rr_score')
        rr_list = os.listdir(inputpath_score2)
        df_rr = pd.DataFrame()
        df_rr['rr'] = rr_list
        df_rr = df_rr[df_rr.rr.str.contains(str(mode_type))]
        df_rr['rr2'] = df_rr['rr'].apply(lambda x: str(x)[:8])
        df_rr = df_rr[df_rr['rr2'] == 'ThisWeek']
        df_rr.sort_values(by='rr')
        try:
           file_name = df_rr['rr'].tolist()[0]
        except:
            file_name=None
            print('找不到' + str(mode_type))
        gt.folder_creator2(outputpath_score2)
        inputpath_score4 = os.path.join(inputpath_score2, 'W' + str(mode_type) + '_his_Ranking.xlsx')
        df_score = pd.read_excel(inputpath_score4, header=None)
        df_score.columns = ['valuation_date', 'code']

        if file_name!=None:
           inputpath_score3 = os.path.join(inputpath_score2, file_name)
           df_score_this = pd.read_excel(inputpath_score3, header=None)
           df_score_this.columns = ['valuation_date', 'code']
        else:
            df_score_this=pd.DataFrame()
        df_score = pd.concat([df_score, df_score_this])
        print(df_score)
        df_score.columns = ['valuation_date', 'code']
        target_end_date='2024-01-01'
        target_end_date2=gt.last_workday_calculate(target_end_date)
        working_day_list=gt.working_days_list('2016-01-01',target_end_date2)
        if self.is_sql == True:
            inputpath_configsql = glv.get('config_sql')
            sm = gt.sqlSaving_main(inputpath_configsql, 'Score',delete=True)
        for available_date in working_day_list:
            available_date2=gt.intdate_transfer(available_date)
            self.logger.info(f'Processing date: {date}')
            # if pd.api.types.is_datetime64_any_dtype(df_score['valuation_date']):
            #     df_score['valuation_date'] = df_score['valuation_date'].dt.strftime('%Y-%m-%d')
            slice_df_score = df_score[df_score['valuation_date'] <= available_date]
            date3=slice_df_score['valuation_date'].unique().tolist()[-1]
            #self.raw_rr_time_checking(date3, date)
            slice_df_score = df_score[df_score['valuation_date'] == date3]
            slice_df_score = gt.rank_score_processing(slice_df_score)
            slice_df_score['valuation_date'] = available_date
            slice_df_score['score_name']='rr_'+str(mode_type)
            outputpath_saving = os.path.join(outputpath_score2, 'rr_' + str(available_date2) + '.csv')
            slice_df_score2 = slice_df_score.copy()
            slice_df_score2['score_name'] = mode_name
            outputpath_saving2 = os.path.join(outputpath_score3, 'rr_' + str(available_date2) + '.csv')
            if len(slice_df_score) > 0:
                slice_df_score2.to_csv(outputpath_saving2, index=False)
                slice_df_score.to_csv(outputpath_saving, index=False)
                if self.is_sql==True:
                    now = datetime.now()
                    slice_df_score['update_time'] = now
                    slice_df_score2['update_time'] = now

                    #capture_file_withdraw_output(sm.df_to_sql, slice_df_score,'score_name','rr_'+str(mode_type))
                    #capture_file_withdraw_output(sm.df_to_sql, slice_df_score2, 'score_name', mode_name)
    def portfolio_info_saving(self):
        df_final=pd.DataFrame()
        inputpath=glv.get('output_portfolio_info')
        df=pd.read_excel(inputpath)
        valuation_date_list=gt.working_days_list(self.start_date,self.end_date)
        for date in valuation_date_list:
            df['valuation_date']=date
            df_final=pd.concat([df_final,df])
        df_final['update_time']=datetime.now()
        inputpath_configsql = glv.get('config_sql')
        sm = gt.sqlSaving_main(inputpath_configsql, 'portfolio_info')
        capture_file_withdraw_output(sm.df_to_sql,df_final)

    def portfolio_info_saving_bu(self):
        df_final=pd.DataFrame()
        inputpath=glv.get('output_portfolio_info_bu')
        df=pd.read_excel(inputpath)
        valuation_date_list=gt.working_days_list(self.start_date,self.end_date)
        for date in valuation_date_list:
            df['valuation_date']=date
            df_final=pd.concat([df_final,df])
        df_final['update_time']=datetime.now()
        inputpath_configsql = glv.get('config_sql')
        sm = gt.sqlSaving_main(inputpath_configsql, 'portfolio_info')
        capture_file_withdraw_output(sm.df_to_sql,df_final)

    def rr_update_main(self):
        self.logger.info('\nStarting RR score update main process...')
        df_config = pd.read_excel(inputpath_score_config)
        df_config['score_type2'] = df_config['score_type'].apply(lambda x: str(x)[:2])
        mode_type_using_list = df_config[df_config['score_type2'] == 'rr']['score_mode'].tolist()
        for mode_type in mode_type_using_list:
            self.raw_rr_updating(mode_type)
        self.portfolio_info_saving()
        self.logger.info('Completed RR score update process')
if __name__ == '__main__':
    #'1094','2063', '1278','1891', '1179','2013','1247', '2227','1130', '1864'
    rr = rrScore_update('2023-01-01', '2025-12-24', is_sql=True)
    rr.portfolio_info_saving_bu()





