from django.shortcuts import render
from django.http import HttpResponse
import top_layout
from login.views import check_login


class Information:
    def __init__(self, title: str | None, text: str) -> None:
        self.title = title
        self.text = text

InfoBlock = str


# Create your views here.
@check_login
def index(request) -> HttpResponse:
    infos: dict[InfoBlock, list[Information]] = {}

    infos['Kde a kdy?'] = [
        Information('Kdy?', 'V sobotu 11. 5. 2024 v 16:45'),
        Information('Kde bude hostina?', '''Victoria Trnava, Štefánikova 35
<br><br>
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2650.0071019787847!2d17.58172937678898!3d48.379599834280576!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x476ca16f9e30ae3d%3A0x173eacf95860fb95!2sVictoria%20Trnava!5e0!3m2!1scs!2scz!4v1682956991370!5m2!1scs!2scz" 
width="90%" height="40%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')
    '''),
        Information('Kde bude obřad?', 'Nebojte se žádného přesouvání, obřad bude na tom stejném místě jako hostina.')]
    
    infos['Co na sebe?'] = [Information('Existují jen 4 pravidla', '''
    <ul>
        <li>Nejdůležitější je, abyste se cítili poholně, mohli tancovat a bavit se.</li>
        <li>Bylo by dobré, kdyby jste se ve svém výběru cítili sebevědomě a měli chuť se s námi vyfotit.</li>
        <li>Dlouhé tylové princeznovské svatební šaty jsou pro všechny kromě nevěsty zakázané.</li>
        <li>Vemte si alespoň spodní prádlo, abych nepohoršovali zaměstnance a Nastina dědu.</li>
    </ul>
    '''),
    Information('Dodatečné doporučení', '''
    <ul>
        <li>Svatba je sice v květnu, ale sál není úplně největší. Počítejte s tím, že tam bude teplo. Doporučujeme tedy tenčí oblečení, případně něco na přehození, pokud chcete vybíhat na terasu a ven.</li>
        <li>Rádi bychom, abyste se trošku hýbali a tancovali, je proto naprosto v pořádku preferovat pohodlnější obuv. Není samozřejmě problém si Vaše oblíbené botky vzít jen na focení a potom se přezout.</li>
    </ul>
    '''),
    Information('Bližší detaily - muži', '''
        V pořádku jsou obleky a košile všech barev a vzorů. Kravaty a motýlci jsou čistě na vašem uvážení a nejsou nijak vyžadovány. 
        Stejně tak není problém vynechat sako.
    '''),
    Information('Bližší detaily - ženy', '''
        <ul>
            <li>Víme, že existuje spoustu názorů na to, jaké barvy se nehodí na svatbu. My žádný takový názor nesdílíme. 
            Není problém si tedy vzít například bílou, červenou, černou, světle modrou, neonově zelenou a vlastně naprosto jakoukoliv.</li>
            <li>Nejsme fanoušci synchronizovaných a zladěných outfitů. Jsme naopak rádi, když se na výběru Vašeho oblečení odráží Váš osobní vkus a styl. Rádi Vás uvidíme v
            krátkých i dlouhých šatech, tričkách či blůzkách se sukněmi nebo nohavicemi, nohavicových kostýmech, dámských oblecích nebo jakýchkoliv jiných kreativních výběrech.
            Stejně tak můžete přijít oblečeni plesově, decentně, moderně, retro, mladistvě, sportově-elegantně, atd.</li>
            <li>Chápeme, že chcete na fotkách vypadat úchvatně a vaše botky musí ladit s celým vaším outfitem, zvažte ale donesení i druhého páru pohodlnějších bot.
            Zejména na několika-hodinovém tancováním se Vám to dost vyplatí. Mnohem radši Vás uvidíme tancovat v plesových šatech a reflexních zelených teniskách, než sedět v lodičkách.</li>
            <li>Pokud máte doma nějaké šaty, co byste si rádi oblékli nebo se Vám nějaké v obchodě zalíbili, ale stále si nejste jisti, zda jsou vážně vhodné, nebojte se nás zeptat. 
            My Vám povíme, že vhodné jsou a budete si je moci obléci bez stresu. Zejména nechceme, aby si někdo zbytečně kupovat šaty, co již nikdy nepoužije,
            nebo hledal jiné, pokud už jedny doma má.</li>
        </ul> 
    ''')
    ]

    infos['Detaily sálu'] = [
        Information('Domácí mazlíčci', 'Zvířátka, ani malá, náš sál nedovoluje. Děti přivést samozřejmě můžete.'),
        Information('Parkování', '''
        Před sálem se bohužel parkovat nedá. Nicméně není problém na daném místě vystoupit z auta nebo z taxíku. 
        Hosté cestující z dálných končin budou moci auta nechat před hotelem, kde budou ubytovaní a v případě potřeby dojet k sálu taxíkem (nebojte se, je to kousek).''' ),
        Information('Uff schody ...', '''No, i na to jsme mysleli. <br>
Záchody, obřadní místo i sál s hostinou jsou v přízemí a se schody se tak prakticky nestřetnete.'''),
        Information('Když je potřeba trochu klidu', '''Čas od času si každý potřebuje odpočinout. Nebudeme to brát jako neslušnost. 
        Pro tyto situace poskytuje areál se sálem i krytou venkovní terasu, kde si budete moci užít ticho, oddechnout si a načerpat síly na další část večera.'''),
        Information('Jak se dostat dovnitř', '''Dveře do areálu nejsou hned z ulice. Je potřeba vejít do pasáže a až tam po pravé straně najdete co hledáte.<br>
Zdá se Vám to moc komplikované? Nebojte, kdybyste se náhodou chtěli ztratit, odchytnou Vás u dveří rodiče nevěsty.'''),
        Information('Kam si sednout', '''Zasedací pořádek si můžete prohlédnout na <a href="/guests#seats">stránce s hosty</a>. 
        Pokud se nemůžete najít, nepanikařte, zasedací pořádek i seznam hostů průběžně aktualizujeme a brzy Vás přidáme.'''),
        Information('Co jsem sem neměl podle Nasti dávat?', 'Vedle záchodů je gauč. To je fajn, protože když náhodou bude na záchod fronta, máte si kam sednout \U0001F606.'),
    ]

    infos['Máme dovoleno fotit?'] = [
        Information(None, '''Focení vám samozřejmě zakázat nemůžeme. Máme však domluveného šikovného fotografa, co bude celý večer dokumentovat,
        fotit párové a skupinové fotky a vlastně cokoliv, co si vymyslíte. Tyto fotografie Vám v nejbližším možném termínu zveřejníme na webových stránkách.
        Budeme tedy rádi, když necháte vaše mazlíčky s bleskem doma, aby se jim nic nestalo a abyste na ně nemuseli dávat pozor.
        ''')
    ]

    infos['Pozornosti'] = [
        Information('Květy', '''Plánujete přinést obrovskou honosnou kytici? A už někdy někdo z Vás musel přenášet z 
        Trnavy do Brna vlakem těch kytic několik a doufat, že se to vejde do malého bytečku? <br>
V této situaci bychom se mohli ocitnout i my a věříme, že toto nikdo nikomu nepřeje. Naopak nás potěší, když jako 
pozornost donese každý jednu růži. Všechny růže se potom budou umísťovat do velké vázy a tak vznike jedna
 obrovská společná kytice, kterou si můžeme s láskou v srdci odnést.'''),
        Information('Svatební dary', '''Lámete si hlavu s tím, co nám vybrat? Nebo naopak už kujete pi  kle a snažíte se nám připravit obrovské překvapení? <br>
Bohužel budeme ještě řádku let bývat v malém bytě, který už nové věci nepojme a transport dárků společně s ostatními věcmi ze svatby by byl přinejmenším komplikovaný. 
To nejdůležitější už přece máme, našli jsme si sami sebe. <br> Pokud byste nás i přesto chtěli obdarovat, budeme rádi za jakýkoliv finanční příspěvek na naši vysněnou svatební cestu.''')
    ]

    context = {'infos': infos, 'top_layout': top_layout.get()}
    return render(request, 'information/index.html', context)
