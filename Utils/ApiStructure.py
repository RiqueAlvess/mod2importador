from typing import Dict
from .FieldConfig import FieldConfig, CategoryConfig, FieldType

class ApiStructure:
    """Estrutura da API organizada e configurável"""
    
    @staticmethod
    def get_structure() -> Dict[str, CategoryConfig]:
        """Retorna a estrutura completa da API"""
        return {
            "identificacao": ApiStructure._get_identificacao_structure(),
            "funcionario": ApiStructure._get_funcionario_structure(),
            "cargo": ApiStructure._get_cargo_structure(),
            "setor": ApiStructure._get_setor_structure(),
            "unidade": ApiStructure._get_unidade_structure(),
            "centro_custo": ApiStructure._get_centro_custo_structure(),
            "turno": ApiStructure._get_turno_structure(),
            "regras_negocio": ApiStructure._get_regras_negocio_structure(),
        }
    
    @staticmethod
    def _get_identificacao_structure() -> CategoryConfig:
        """Configuração dos campos de identificação"""
        return CategoryConfig(
            key="identificacao",
            title="Identificação da API",
            description="Configurações de autenticação e identificação",
            required=True,
            icon="🔐",
            order=1,
            fields={
                "chaveAcesso": FieldConfig(
                    name="chaveAcesso",
                    display_name="Chave de Acesso",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Chave de acesso para autenticação na API"
                ),
                "codigoEmpresaPrincipal": FieldConfig(
                    name="codigoEmpresaPrincipal",
                    display_name="Código Empresa Principal",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Código da empresa principal no sistema"
                ),
                "codigoResponsavel": FieldConfig(
                    name="codigoResponsavel",
                    display_name="Código Responsável",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Código do responsável pela operação"
                ),
                "codigoUsuario": FieldConfig(
                    name="codigoUsuario",
                    display_name="Código Usuário",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Código do usuário responsável pela ação"
                )
            }
        )
    
    @staticmethod
    def _get_funcionario_structure() -> CategoryConfig:
        """Configuração dos campos do funcionário"""
        return CategoryConfig(
            key="funcionario",
            title="Dados do Funcionário",
            description="Informações pessoais e profissionais do funcionário",
            required=True,
            icon="👤",
            order=2,
            fields={
                "nomeFuncionario": FieldConfig(
                    name="nomeFuncionario",
                    display_name="Nome Completo",
                    field_type=FieldType.STRING,
                    required=True,
                    max_length=120,
                    description="Nome completo do funcionário"
                ),
                "cpf": FieldConfig(
                    name="cpf",
                    display_name="CPF",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=15,
                    validation_rules=["validate_cpf"],
                    format_pattern="###.###.###-##",
                    description="CPF do funcionário"
                ),
                "dataNascimento": FieldConfig(
                    name="dataNascimento",
                    display_name="Data de Nascimento",
                    field_type=FieldType.DATE,
                    required=True,
                    format_pattern="dd/mm/yyyy",
                    description="Data de nascimento do funcionário"
                ),
                "sexo": FieldConfig(
                    name="sexo",
                    display_name="Sexo",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["MASCULINO", "FEMININO"],
                    description="Sexo do funcionário"
                ),
                "estadoCivil": FieldConfig(
                    name="estadoCivil",
                    display_name="Estado Civil",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["SOLTEIRO", "CASADO", "SEPARADO", "DIVORCIADO", "VIUVO", "OUTROS", "DESQUITADO", "UNIAO_ESTAVEL"],
                    description="Estado civil do funcionário"
                ),
                "dataAdmissao": FieldConfig(
                    name="dataAdmissao",
                    display_name="Data de Admissão",
                    field_type=FieldType.DATE,
                    required=True,
                    format_pattern="dd/mm/yyyy",
                    description="Data de admissão do funcionário"
                ),
                "regimeTrabalho": FieldConfig(
                    name="regimeTrabalho",
                    display_name="Regime de Trabalho",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["NORMAL", "TURNO"],
                    description="Regime de trabalho do funcionário"
                ),
                "tipoContratacao": FieldConfig(
                    name="tipoContratacao",
                    display_name="Tipo de Contratação",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CLT", "COOPERADO", "TERCERIZADO", "AUTONOMO", "TEMPORARIO", "PESSOA_JURIDICA", "ESTAGIARIO", "MENOR_APRENDIZ"],
                    description="Tipo de contratação do funcionário"
                ),
                "chaveProcuraFuncionario": FieldConfig(
                    name="chaveProcuraFuncionario",
                    display_name="Chave de Busca",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CODIGO", "MATRICULA", "MATRICULA_RH", "CPF", "DATA_NASCIMENTO", "CPF_PENDENTE", "CPF_ATIVO"],
                    description="Chave utilizada para buscar o funcionário"
                ),
                "codigoEmpresa": FieldConfig(
                    name="codigoEmpresa",
                    display_name="Código da Empresa",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Código da empresa onde trabalha o funcionário"
                ),
                "tipoBuscaEmpresa": FieldConfig(
                    name="tipoBuscaEmpresa",
                    display_name="Tipo Busca Empresa",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CODIGO_SOC", "CODIGO_CLIENTE"],
                    description="Tipo de busca para localizar a empresa"
                ),
                "situacao": FieldConfig(
                    name="situacao",
                    display_name="Situação",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["ATIVO", "AFASTADO", "PENDENTE", "FERIAS", "INATIVO"],
                    description="Situação atual do funcionário"
                ),
                "matricula": FieldConfig(
                    name="matricula",
                    display_name="Matrícula",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=30,
                    description="Matrícula do funcionário"
                ),
                "email": FieldConfig(
                    name="email",
                    display_name="Email",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=400,
                    validation_rules=["validate_email"],
                    description="Email do funcionário"
                ),
                "telefoneResidencial": FieldConfig(
                    name="telefoneResidencial",
                    display_name="Telefone Residencial",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=15,
                    validation_rules=["validate_phone"],
                    description="Telefone residencial do funcionário"
                ),
                "telefoneCelular": FieldConfig(
                    name="telefoneCelular",
                    display_name="Telefone Celular",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=15,
                    validation_rules=["validate_phone"],
                    description="Telefone celular do funcionário"
                ),
                "endereco": FieldConfig(
                    name="endereco",
                    display_name="Endereço",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=110,
                    description="Endereço do funcionário"
                ),
                "bairro": FieldConfig(
                    name="bairro",
                    display_name="Bairro",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=80,
                    description="Bairro onde habita o funcionário"
                ),
                "cidade": FieldConfig(
                    name="cidade",
                    display_name="Cidade",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=50,
                    description="Cidade onde habita o funcionário"
                ),
                "estado": FieldConfig(
                    name="estado",
                    display_name="Estado",
                    field_type=FieldType.ENUM,
                    required=False,
                    enum_values=["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"],
                    description="Estado onde habita o funcionário"
                ),
                "cep": FieldConfig(
                    name="cep",
                    display_name="CEP",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=8,
                    format_pattern="#####-###",
                    description="CEP do funcionário"
                )
            }
        )
    
    @staticmethod
    def _get_cargo_structure() -> CategoryConfig:
        """Configuração dos campos do cargo"""
        return CategoryConfig(
            key="cargo",
            title="Cargo",
            description="Informações sobre o cargo do funcionário",
            required=False,
            icon="💼",
            order=3,
            fields={
                "nome": FieldConfig(
                    name="nome",
                    display_name="Nome do Cargo",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=130,
                    description="Nome do cargo"
                ),
                "codigo": FieldConfig(
                    name="codigo",
                    display_name="Código",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=9,
                    description="Código do cargo no SOC"
                ),
                "codigoRh": FieldConfig(
                    name="codigoRh",
                    display_name="Código RH",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=80,
                    description="Código utilizado pela empresa para o cargo"
                ),
                "cbo": FieldConfig(
                    name="cbo",
                    display_name="CBO",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=10,
                    description="Classificação Brasileira de Ocupações"
                ),
                "descricaoDetalhada": FieldConfig(
                    name="descricaoDetalhada",
                    display_name="Descrição Detalhada",
                    field_type=FieldType.TEXT,
                    required=False,
                    description="Descrição detalhada do cargo"
                ),
                "tipoBusca": FieldConfig(
                    name="tipoBusca",
                    display_name="Tipo de Busca",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CODIGO", "CODIGO_RH", "NOME"],
                    description="Tipo de busca para localizar o cargo"
                )
            }
        )
    
    @staticmethod
    def _get_setor_structure() -> CategoryConfig:
        """Configuração dos campos do setor"""
        return CategoryConfig(
            key="setor",
            title="Setor",
            description="Informações sobre o setor do funcionário",
            required=False,
            icon="🏢",
            order=4,
            fields={
                "nome": FieldConfig(
                    name="nome",
                    display_name="Nome do Setor",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=130,
                    description="Nome do setor"
                ),
                "codigo": FieldConfig(
                    name="codigo",
                    display_name="Código",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=8,
                    description="Código do setor no SOC"
                ),
                "codigoRh": FieldConfig(
                    name="codigoRh",
                    display_name="Código RH",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=80,
                    description="Código do setor utilizado pela empresa"
                ),
                "descricao": FieldConfig(
                    name="descricao",
                    display_name="Descrição",
                    field_type=FieldType.TEXT,
                    required=False,
                    description="Descrição do setor"
                ),
                "tipoBusca": FieldConfig(
                    name="tipoBusca",
                    display_name="Tipo de Busca",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CODIGO", "CODIGO_RH", "NOME"],
                    description="Tipo de busca para localizar o setor"
                )
            }
        )
    
    @staticmethod
    def _get_unidade_structure() -> CategoryConfig:
        """Configuração dos campos da unidade"""
        return CategoryConfig(
            key="unidade",
            title="Unidade",
            description="Informações sobre a unidade do funcionário",
            required=False,
            icon="🏭",
            order=5,
            fields={
                "nome": FieldConfig(
                    name="nome",
                    display_name="Nome da Unidade",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=130,
                    description="Nome da unidade"
                ),
                "codigo": FieldConfig(
                    name="codigo",
                    display_name="Código",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=20,
                    description="Código da unidade no SOC"
                ),
                "codigoRh": FieldConfig(
                    name="codigoRh",
                    display_name="Código RH",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=80,
                    description="Código da unidade utilizado na empresa"
                ),
                "tipoBusca": FieldConfig(
                    name="tipoBusca",
                    display_name="Tipo de Busca",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CODIGO", "CODIGO_RH", "NOME"],
                    description="Tipo de busca para localizar a unidade"
                )
            }
        )
    
    @staticmethod
    def _get_centro_custo_structure() -> CategoryConfig:
        """Configuração dos campos do centro de custo"""
        return CategoryConfig(
            key="centro_custo",
            title="Centro de Custo",
            description="Informações sobre o centro de custo",
            required=False,
            icon="💰",
            order=6,
            fields={
                "nome": FieldConfig(
                    name="nome",
                    display_name="Nome do Centro de Custo",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=130,
                    description="Nome do centro de custo"
                ),
                "codigo": FieldConfig(
                    name="codigo",
                    display_name="Código",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=20,
                    description="Código do centro de custo no SOC"
                ),
                "codigoRh": FieldConfig(
                    name="codigoRh",
                    display_name="Código RH",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=80,
                    description="Código do centro de custo utilizado pela empresa"
                ),
                "tipoBusca": FieldConfig(
                    name="tipoBusca",
                    display_name="Tipo de Busca",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CODIGO", "CODIGO_RH", "NOME"],
                    description="Tipo de busca para localizar o centro de custo"
                )
            }
        )
    
    @staticmethod
    def _get_turno_structure() -> CategoryConfig:
        """Configuração dos campos do turno"""
        return CategoryConfig(
            key="turno",
            title="Turno",
            description="Informações sobre o turno do funcionário",
            required=False,
            icon="🕐",
            order=7,
            fields={
                "nome": FieldConfig(
                    name="nome",
                    display_name="Nome do Turno",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=100,
                    description="Nome do turno"
                ),
                "codigo": FieldConfig(
                    name="codigo",
                    display_name="Código",
                    field_type=FieldType.INTEGER,
                    required=False,
                    description="Código do turno no SOC"
                ),
                "codigoRh": FieldConfig(
                    name="codigoRh",
                    display_name="Código RH",
                    field_type=FieldType.STRING,
                    required=False,
                    max_length=100,
                    description="Código do turno utilizado na empresa"
                ),
                "tipoBusca": FieldConfig(
                    name="tipoBusca",
                    display_name="Tipo de Busca",
                    field_type=FieldType.ENUM,
                    required=True,
                    enum_values=["CODIGO", "NOME", "CODIGO_RH"],
                    description="Tipo de busca para localizar o turno"
                )
            }
        )
    
    @staticmethod
    def _get_regras_negocio_structure() -> CategoryConfig:
        """Configuração das regras de negócio"""
        return CategoryConfig(
            key="regras_negocio",
            title="Regras de Negócio",
            description="Configurações que controlam o comportamento da importação",
            required=False,
            icon="⚙️",
            order=8,
            fields={
                "criarFuncionario": FieldConfig(
                    name="criarFuncionario",
                    display_name="Criar Funcionário",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o funcionário deve ser criado caso não seja encontrado"
                ),
                "atualizarFuncionario": FieldConfig(
                    name="atualizarFuncionario",
                    display_name="Atualizar Funcionário",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o cadastro do funcionário deve ser atualizado"
                ),
                "criarCargo": FieldConfig(
                    name="criarCargo",
                    display_name="Criar Cargo",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o cargo deve ser criado caso não seja encontrado"
                ),
                "atualizarCargo": FieldConfig(
                    name="atualizarCargo",
                    display_name="Atualizar Cargo",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o cadastro do cargo deve ser atualizado"
                ),
                "criarSetor": FieldConfig(
                    name="criarSetor",
                    display_name="Criar Setor",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o setor deve ser criado caso não seja encontrado"
                ),
                "atualizarSetor": FieldConfig(
                    name="atualizarSetor",
                    display_name="Atualizar Setor",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o cadastro do setor deve ser atualizado"
                ),
                "criarUnidade": FieldConfig(
                    name="criarUnidade",
                    display_name="Criar Unidade",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se a unidade deve ser criada caso não seja encontrada"
                ),
                "atualizarUnidade": FieldConfig(
                    name="atualizarUnidade",
                    display_name="Atualizar Unidade",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o cadastro da unidade deve ser atualizado"
                ),
                "criarCentroCusto": FieldConfig(
                    name="criarCentroCusto",
                    display_name="Criar Centro de Custo",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o centro de custo deve ser criado caso não seja encontrado"
                ),
                "atualizarCentroCusto": FieldConfig(
                    name="atualizarCentroCusto",
                    display_name="Atualizar Centro de Custo",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o cadastro do centro de custo deve ser atualizado"
                ),
                "criarTurno": FieldConfig(
                    name="criarTurno",
                    display_name="Criar Turno",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o turno deve ser criado caso não seja encontrado"
                ),
                "atualizarTurno": FieldConfig(
                    name="atualizarTurno",
                    display_name="Atualizar Turno",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o cadastro do turno deve ser atualizado"
                ),
                "criarHistorico": FieldConfig(
                    name="criarHistorico",
                    display_name="Criar Histórico",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se o histórico deve ser criado durante a importação"
                ),
                "naoImportarFuncionarioSemHierarquia": FieldConfig(
                    name="naoImportarFuncionarioSemHierarquia",
                    display_name="Não Importar Sem Hierarquia",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se não deve importar funcionário sem hierarquia completa"
                ),
                "destravarFuncionarioBloqueado": FieldConfig(
                    name="destravarFuncionarioBloqueado",
                    display_name="Destravar Funcionário Bloqueado",
                    field_type=FieldType.BOOLEAN,
                    required=False,
                    description="Indica se deve destravar funcionário bloqueado"
                )
            }
        )
