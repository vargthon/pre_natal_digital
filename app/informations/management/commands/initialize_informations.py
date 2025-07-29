from django.core.management.base import BaseCommand
from informations.models import Information

class Command(BaseCommand):
    help = 'Initialize the Information model with default data'

    def handle(self, *args, **kwargs):
        # Check if any Information instances already exist
        if Information.objects.exists():
            self.stdout.write(self.style.WARNING('Information instances already exist. Skipping initialization.'))
            return

        # Create default Information instances
        default_data = [
            {
                'title': 'Descoberta da Gravidez',
                'description': (
                    "## Descoberta da Gravidez\n\n"
                    "A descoberta da gravidez é um momento marcante na vida de muitas pessoas. "
                    "Os primeiros sinais podem incluir atraso menstrual, náuseas, sensibilidade nos seios e cansaço. "
                    "Para confirmar a gestação, recomenda-se realizar um teste de farmácia ou procurar um profissional de saúde para exames laboratoriais.\n\n"
                    "### O que fazer após a descoberta?\n"
                    "- Marque uma consulta pré-natal.\n"
                    "- Adote hábitos saudáveis, como alimentação equilibrada e prática de exercícios leves.\n"
                    "- Evite o consumo de álcool, cigarro e outras substâncias prejudiciais.\n"
                    "- Tire dúvidas com profissionais de saúde e busque apoio emocional.\n\n"
                    "Acompanhe cada etapa dessa nova jornada com informação e cuidado!"
                ),
                'order': 1,
            },
            {
                'title': 'Cuidados na Gravidez',
                'description': (
                    "## Cuidados na Gravidez\n\n"
                    "Durante a gravidez, é essencial cuidar da saúde física e emocional. "
                    "Algumas recomendações incluem:\n\n"
                    "- **Alimentação saudável:** Inclua frutas, verduras, grãos integrais e proteínas magras.\n"
                    "- **Hidratação:** Beba bastante água para manter-se hidratada.\n"
                    "- **Exercícios físicos:** Pratique atividades leves, como caminhadas, sempre com orientação médica.\n"
                    "- **Descanso:** Priorize o sono e momentos de relaxamento.\n"
                    "- **Consultas médicas regulares:** Realize o pré-natal conforme as orientações do profissional de saúde.\n\n"
                    "Lembre-se: cada gravidez é única. Consulte sempre seu médico para orientações personalizadas."
                ),
                'order': 2,
            },
            {
                'title': 'Alimentação Saudável na Gravidez',
                'description': (
                    "## Alimentação Saudável na Gravidez\n\n"
                    "Uma alimentação equilibrada é fundamental para a saúde da gestante e do bebê. "
                    "Algumas dicas incluem:\n\n"
                    "- **Variedade de alimentos:** Inclua diferentes grupos alimentares para garantir todos os nutrientes.\n"
                    "- **Ácido fólico:** Consuma alimentos ricos em ácido fólico, como folhas verdes, feijão e laranja.\n"
                    "- **Cálcio:** Priorize laticínios, vegetais verdes e peixes para fortalecer ossos e dentes.\n"
                    "- **Hidratação:** Beba água regularmente para evitar desidratação.\n\n"
                    "Evite alimentos processados, ricos em açúcar e gordura saturada. Consulte um nutricionista para orientações específicas."
                ),
                'order': 3,
            },
            {                'title': 'Exercícios Físicos na Gravidez',
                'description': (
                    "## Exercícios Físicos na Gravidez\n\n"
                    "A prática de exercícios físicos durante a gravidez pode trazer diversos benefícios, como:\n\n"
                    "- **Melhora da circulação sanguínea:** Ajuda a reduzir o inchaço e melhora a disposição.\n"
                    "- **Controle do ganho de peso:** Contribui para uma gestação saudável.\n"
                    "- **Redução do estresse:** Promove o bem-estar emocional.\n"
                    "- **Preparação para o parto:** Fortalece os músculos e melhora a resistência.\n\n"
                    "Consulte sempre seu médico antes de iniciar qualquer atividade física e escolha exercícios adequados para gestantes, como caminhadas, natação e yoga."
                ),
                'order': 4,
            },
          
        ]

        for data in default_data:
            Information.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully initialized Information model with default data.'))
