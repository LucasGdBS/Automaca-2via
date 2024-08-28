import undetected_chromedriver as uc
from decouple import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

project_directory = os.path.dirname(os.path.abspath(__file__))
download_directory = os.path.join(project_directory, "downloads")

os.makedirs(download_directory, exist_ok=True)


class Bot:
	def __init__(self, cpf_cnpj, password, conta_contrato=None):
		self.url = config('URL_NEOENERGIA')
		self.driver = None
		self.cpf_cnpj = self.cpf_format(cpf_cnpj)
		self.password = password
		self.conta_contrato = conta_contrato

		self.options = uc.ChromeOptions()
		self.options.add_argument('--disable-save-password-bubble')
		self.options.add_argument('--password-store=basic')
		self.options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
						
			"download.default_directory": download_directory,
			"download.prompt_for_download": False,
			"download.directory_upgrade": True,
    		"plugins.always_open_pdf_externally": True
        },
    )
	
	def cpf_format(self, cpf):
		if len(cpf) == 11:
			return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
		elif len(cpf) == 14:
			return f'{cpf[:2]}.{cpf[2:5]}.{cpf[5:8]}/{cpf[8:12]}-{cpf[12:]}'
		else:
			raise ValueError('CPF ou CNPJ inválido. Insira sem pontos, traços ou barras.')
        
	def init_driver(self):
		self.driver = uc.Chrome(options=self.options)
		self.driver.delete_all_cookies()
		self.driver.maximize_window()
		self.driver.implicitly_wait(10)
		self.wait = WebDriverWait(self.driver, 5)
	
	def login(self):
		self.init_driver()
		self.driver.get(self.url)

		# Login
		panel_login = self.driver.find_element(By.ID, 'panel-login')
		form_group = panel_login.find_element(By.CLASS_NAME, 'form-group')

		# CPF ou CNPJ
		cpf = form_group.find_element(By.ID, 'ctl00_SPWebPartManager1_g_c51f1176_88d3_45f0_973b_55115dca106b_ctl00_txtCNPJ_CPF')
		cpf.send_keys(self.cpf_cnpj)

		# Senha
		password = form_group.find_element(By.ID, 'ctl00_SPWebPartManager1_g_c51f1176_88d3_45f0_973b_55115dca106b_ctl00_txtSenha')
		password.send_keys(self.password)

		# Entrar
		enter_button = panel_login.find_element(By.CLASS_NAME, 'btn')
		enter_button.click()

	def find_contract(self):

		# Acessar o contrato
		table = self.driver.find_element(By.CLASS_NAME, 'table')
		rows = table.find_elements(By.TAG_NAME, 'tr')

		for row in rows:
			cells = row.find_elements(By.TAG_NAME, 'td')
			if len(cells) > 0:
				if cells[1].text == self.conta_contrato or self.conta_contrato is None:
					cells[0].find_element(By.TAG_NAME, 'input').click()
					return
		raise ValueError('Contrato não encontrado.')
	
	def select_option(self):
		self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'dfwp-item')))
		self.driver.get('https://servicos.neoenergiapernambuco.com.br/servicos-ao-cliente/Pages/2-via-conta_anti.aspx')
	
	def acess_pdf(self):
		self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
		iframe = self.driver.find_element(By.CSS_SELECTOR, "div#ctl00_m_g_df32160e_0cad_4a26_927a_6186cce39149 iframe")

		self.driver.switch_to.frame(iframe)
		img_element = self.wait.until(
    		EC.presence_of_element_located((By.CSS_SELECTOR, "img.tipViaPgto"))
		)
		img_element.click()
		self.driver.switch_to.default_content()

		# Troca de aba
		tabs = self.driver.window_handles
		self.driver.switch_to.window(tabs[-1])

		input_element = WebDriverWait(self.driver, 10).until(
    		EC.element_to_be_clickable((By.XPATH, "//table[@class='neoNNtab00']//tr[last()]/td/input[@id='btn_naofaturamao']"))
		)
		input_element.click()
		sleep(5)
		
	def second_bill_copy(self):		
		self.login()
		self.find_contract()
		self.select_option()
		self.acess_pdf()

		self.driver.quit()


bot = Bot(config('CPF_CNPJ'), config('PASSWORD'), conta_contrato=config('CONTA_CONTRATO'))
bot.second_bill_copy()