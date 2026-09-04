import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUT_DIR = "/Users/howardliao/legal_strategy_project"
doc_path = os.path.join(OUT_DIR, "legal_strategy_report.docx")

doc = Document()

# Page setup: A4, 20mm margins
for section in doc.sections:
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(22)
    section.right_margin = Mm(22)

# Colors
COLOR_RUST = RGBColor(168, 50, 18)     # #A83212 鐵鏽
COLOR_ORANGE = RGBColor(222, 88, 20)   # #DE5814 標題橘
COLOR_AMBER = RGBColor(217, 119, 6)    # #D97706 重點琥珀黃
COLOR_CITRUS = RGBColor(234, 88, 12)   # #EA580C 柑橘
COLOR_CHARCOAL = RGBColor(45, 55, 72)  # #2D3748 黑灰色內文
FONT_FAMILY = "PingFang TC"            # 粗圓/黑體/優質無襯線

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_title(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level==1 else 10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = FONT_FAMILY
    run.font.bold = True
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = COLOR_ORANGE
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_RUST
    else:
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_CITRUS
    return p

def add_body_p(text_runs):
    # text_runs is list of tuples: (text, is_highlight, is_bold)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    for item in text_runs:
        if isinstance(item, str):
            text, is_hl, is_b = item, False, False
        else:
            text = item[0]
            is_hl = item[1] if len(item) > 1 else False
            is_b = item[2] if len(item) > 2 else False
        
        run = p.add_run(text)
        run.font.name = FONT_FAMILY
        run.font.bold = is_b or is_hl
        run.font.size = Pt(10.5)
        if is_hl:
            run.font.color.rgb = COLOR_AMBER
        else:
            run.font.color.rgb = COLOR_CHARCOAL
    return p

# ----------------- COVER PAGE -----------------
cover_p = doc.add_paragraph()
cover_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
cover_p.paragraph_format.space_before = Pt(20)
cover_p.paragraph_format.space_after = Pt(10)

art_path = os.path.join(OUT_DIR, "pharaoh_cover_art.png")
if os.path.exists(art_path):
    doc.add_picture(art_path, width=Inches(5.5))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    last_p.paragraph_format.space_after = Pt(15)

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_before = Pt(10)
title_p.paragraph_format.space_after = Pt(6)
t_run = title_p.add_run("八旬失智配偶法律權益保全與離婚訴訟戰略報告")
t_run.font.name = FONT_FAMILY
t_run.font.size = Pt(22)
t_run.font.bold = True
t_run.font.color.rgb = COLOR_ORANGE

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(20)
s_run = sub_p.add_run("阻斷惡意脫產・夫妻剩餘財產清算・監護宣告・追討第三者・權益最大化全指南")
s_run.font.name = FONT_FAMILY
s_run.font.size = Pt(12)
s_run.font.bold = True
s_run.font.color.rgb = COLOR_RUST

div_path = os.path.join(OUT_DIR, "egypt_divider.png")
if os.path.exists(div_path):
    doc.add_picture(div_path, width=Inches(5.2))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    last_p.paragraph_format.space_after = Pt(25)

# Reporter Box
rep_table = doc.add_table(rows=1, cols=1)
rep_table.alignment = WD_TABLE_ALIGNMENT.CENTER
cell = rep_table.cell(0, 0)
set_cell_shading(cell, "FFFBEB") # warm amber wash
set_cell_margins(cell, 180, 180, 300, 300)
rp = cell.paragraphs[0]
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_run1 = rp.add_run("報告人：Howard Liao Ph.D.(廖倫豪 博士)\n")
r_run1.font.name = FONT_FAMILY
r_run1.font.size = Pt(13)
r_run1.font.bold = True
r_run1.font.color.rgb = COLOR_ORANGE

r_run2 = rp.add_run("家事法規與權益實務戰略專案 ｜ 日期：2026年9月")
r_run2.font.name = FONT_FAMILY
r_run2.font.size = Pt(10)
r_run2.font.color.rgb = COLOR_CHARCOAL

doc.add_page_break()

# ----------------- CHAPTER 1 -----------------
add_title("第一章：醫療端關鍵診斷證明開立指引（台中榮總就醫）", level=1)
add_body_p([
    ("針對母親罹患腦部退化（失智症），且目前已具備申請外籍看護資格之現況，前往台中榮總神經內科由其他主治醫師接替看診時，必須同步辦妥以下兩大法律與福利證明：", False, False)
])

add_title("1.1 申辦【身心障礙證明（殘障手冊）】（看診前先備表）", level=2)
add_body_p([
    ("• ", False, False),
    ("辦理程序：", True, True),
    ("身心障礙證明依法由地方政府社會局核發，醫院負責醫療鑑定。為避免多跑一趟，家屬請於看診前攜帶母親身分證正本、印章、1吋照片3張及代辦人證件，至戶籍地區公所社會課領取空白的「身心障礙者鑑定表」。", False, False)
])
add_body_p([
    ("• ", False, False),
    ("診間落實：", True, True),
    ("看診當天直接將鑑定表交由看診醫師。醫師調閱台中榮總歷史病歷與腦部影像即可完成第一階段生理評估，院內身心障礙鑑定窗口（第一醫療大樓一樓大廳）將於當日或7日內接續完成生活功能評估，並由醫院專函送交衛生局審查發證。", False, False)
])
add_body_p([
    ("• ", False, False),
    ("實質效益：", True, True),
    ("每年享綜合所得稅特別扣除額21.8萬元、健保自付額減免（中度減半、重度全免）、牌照稅減免，且取得重度以上證明可直接享有免繳聘僱外籍看護每月2,000元就業安定費之實質經濟優惠。", False, False)
])

add_title("1.2 開立訴訟防禦專用【乙種診斷證明書】", level=2)
add_body_p([
    ("向接診醫師申請診斷證明書時，務必請醫師在診斷與醫囑欄中載明以下四大關鍵法律要件，作為法庭上無可辯駁之鐵證：", False, False)
])

# 4 Key Points Table
doc_tbl = doc.add_table(rows=5, cols=2)
doc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["關鍵要素", "具體文字與訴訟防禦效果"]
for i, h in enumerate(headers):
    c = doc_tbl.cell(0, i)
    set_cell_shading(c, "FEF3C7")
    set_cell_margins(c, 100, 100, 140, 140)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.color.rgb = COLOR_RUST

row_data = [
    ("精確病名與病程", "載明失智症／腦退化學名，並註明「長期於台中榮總規則治療追蹤」，證實病況為不可逆之神經退化，非人為故意所致。"),
    ("量表數據（CDR／MMSE）", "明確註記 CDR（臨床失智評估量表）分數（如 CDR=1、2或3分）與 MMSE 分數，為外勞新制免評與法律能力之客觀標準。"),
    ("喪失意思與辨識能力", "載明「認知功能嚴重減退，致不能辨識其行為或缺乏獨立處理自己事務之能力」。阻斷父親私下哄騙母親簽署離婚協議或財產過戶。"),
    ("生活全無自理需全天照護", "載明「日常生活無自理能力，需24小時專人全天候監護照顧」。日後向父親索求每月扶養費、看護費與高額贍養費之鐵證。")
]

for row_idx, (col1, col2) in enumerate(row_data, start=1):
    c1, c2 = doc_tbl.cell(row_idx, 0), doc_tbl.cell(row_idx, 1)
    set_cell_shading(c1, "FFFDF7" if row_idx % 2 == 0 else "FFFFFF")
    set_cell_shading(c2, "FFFDF7" if row_idx % 2 == 0 else "FFFFFF")
    set_cell_margins(c1, 90, 90, 120, 120)
    set_cell_margins(c2, 90, 90, 120, 120)
    p1 = c1.paragraphs[0].add_run(col1)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_AMBER
    p2 = c2.paragraphs[0].add_run(col2)
    p2.font.color.rgb = COLOR_CHARCOAL

# ----------------- CHAPTER 2 -----------------
add_title("第二章：緊急法律止血與防禦程序（第一時間阻斷脫產）", level=1)

add_title("2.1 第一要務：立刻向家事法院聲請「監護宣告」", level=2)
add_body_p([
    ("• ", False, False),
    ("法律依據：", True, True),
    ("民法第 14 條及家事事件法規定。母親因神經退化失智已無法為有效之意思表示。", False, False)
])
add_body_p([
    ("• ", False, False),
    ("作戰效果：", True, True),
    ("由子女（您）出任法定監護人兼法定代理人。裁定後，母親名下財產受法院嚴格監護，", False, False),
    ("父親無法私下誘導母親辦理協議離婚或將房地產贈與他人", True, True),
    ("；在未來所有民事與家事訴訟中，均由監護人代表母親出庭應訊，確保權益滴水不漏。", False, False)
])

add_title("2.2 全面清查父親底牌：向國稅局調閱財產總歸戶清單", level=2)
add_body_p([
    ("持監護人身分或受任代理文件，前往國稅局申請父親與母親雙方之「全國財產稅總歸戶財產查詢清單」與「近三年綜合所得稅各類所得清單」。", False, False)
])
add_body_p([
    ("清查重點包括：所有不動產地號建號、上市櫃股票集保庫存、銀行大額存款利息來源帳戶。此舉能立即鎖定父親現存之總資產基數，作為剩餘財產分配請求權之計算基準。", False, False)
])

add_title("2.3 聲請「假扣押／家事暫時處分」凍結名下資產", level=2)
add_body_p([
    ("外遇方最常見的脫法行為即為私下出售房屋、解約定存或無償贈與第三者。律師應以侵害配偶權賠償金、剩餘財產分配為由，向法院聲請裁定對父親名下不動產與主要帳戶進行", False, False),
    ("暫時處分或假扣押查封", True, True),
    ("，防止資產於訴訟期間遭暗中搬空。", False, False)
])

# ----------------- CHAPTER 3 -----------------
add_title("第三章：爭取母親權益與金錢賠償最大化（四大求償途徑）", level=1)

add_title("3.1 夫妻剩餘財產分配請求權（民法第 1030 條之 1）——金額最大宗（佔比 90% 以上）", level=2)
add_body_p([
    ("法定財產制關係消滅時，夫或妻現存之婚後財產扣除負債後，雙方差額應平均分配。以八十歲夫妻之婚後積累而言，父親名下之房產增值、退休金存款及股票均屬分配範圍。母親依法享有", False, False),
    ("差額之 50% 請求權", True, True),
    ("，這是確保母親晚年高額經濟保障的最核心支柱。", False, False)
])

add_title("3.2 致命殺手鐧：追討小三條款（民法第 1030 條之 3 追加計算）", level=2)
add_body_p([
    ("若父親在提出離婚前", False, False),
    ("五年內", True, True),
    ("，企圖減少剩餘財產分配而將資產贈與小三（如購屋登記小三名下、大額資金無償匯款），法律明定", False, False),
    ("「應將該贈與財產全數追加計算，視為父親現存之婚後財產」", True, True),
    ("！縱使父親名下故意脫產一空，法院仍會將贈與小三的金額加回計算，判令父親自現有資產或由小三承擔返還責任（民法第 1020-1 條撤銷權）。", False, False)
])

add_title("3.3 共同控告父親與小三「侵害配偶權」（民法第 184 條、第 195 條）", level=2)
add_body_p([
    ("將小三與父親列為連帶共同被告。蒐集兩人同居進出、親密合照、牽手出遊、通訊對話等實質破壞婚姻生活之證據。法院審酌雙方資力及八旬原配病中遭背叛之重大精神痛苦，連帶精神慰撫金實務判賠金額普遍在", False, False),
    ("30 萬 ～ 100 萬元", True, True),
    ("不等，由兩人負連帶清償責任。", False, False)
])

add_title("3.4 判決離婚損害賠償（民法第 1056 條）與終身贍養費（民法第 1057 條）", level=2)
add_body_p([
    ("• 離婚過失賠償：因父親可歸責之事由致離婚，母親得請求單獨之精神損害賠償（30萬～80萬）。", False, False)
])
add_body_p([
    ("• 終身照護贍養費：母親八旬失智、無自理與謀生能力，因判決離婚陷於重大照護困難。法院將審酌外籍看護月薪（約3.5萬）、醫療耗材、安養費用，判命父親按月給付高額生活扶養費或一次性支付大額贍養基金。", False, False)
])

# ----------------- CHAPTER 4 -----------------
add_title("第四章：八旬長輩核心戰略抉擇——「離」與「不離」的極限博弈", level=1)

add_body_p([
    ("雙方年逾八旬，在法律實戰中，「堅決不離婚」與「反訴離婚」各有極為顯著之戰略優劣，應視父親資產流動性與脫產風險精準抉擇：", False, False)
])

matrix_tbl = doc.add_table(rows=3, cols=3)
matrix_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
m_headers = ["戰略方案", "法律策略與操作重點", "權益最大化效益評估"]
for idx, h in enumerate(m_headers):
    c = matrix_tbl.cell(0, idx)
    set_cell_shading(c, "FEF3C7")
    set_cell_margins(c, 100, 100, 120, 120)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.color.rgb = COLOR_RUST

m_rows = [
    ("策略 A：堅決不離\n（以拖待變・遺產保全）",
     "1. 依民法第 1052 條第 2 項但書，外遇有過失方無權強逼無過失重病原配離婚。\n2. 向法院聲請裁定「給付家庭生活費暫時處分」，強制父親每月按時匯入外勞看護費與生活開銷。\n3. 保全通姦證據，單獨訴請父親與小三賠償侵害配偶權。",
     "【終極最大利益】\n母親完整保留合法配偶之第一順位法定繼承權！\n日後父親百年之時，母親可先主張「夫妻剩餘財產分一半」，再與全體子女均分剩餘遺產。小三在法律上為局外人，一毛遺產皆無權繼承！"),
    ("策略 B：同意／反訴離婚\n（即刻落袋・強制清算）",
     "1. 發現父親正在加速轉賣不動產、洗錢移轉資產給小三，拖延恐遭完全脫產。\n2. 即刻發動反訴，全面聲請假扣押凍結所有已知房產與存款。\n3. 主張剩餘財產差額半數＋民法1030-3追討追加＋高額贍養費＋精神慰撫金。",
     "【落袋為安・徹底切割】\n透過法院強制執行程序，直接將數千萬之現金存款與房屋產權登記回母親名下。\n由監護人（子女）設立安養照護專用安養信託，確保母親晚年尊嚴與醫療照料無虞。")
]

for r_i, r_data in enumerate(m_rows, start=1):
    for c_i, text in enumerate(r_data):
        c = matrix_tbl.cell(r_i, c_i)
        set_cell_shading(c, "FFFDF7" if r_i % 2 == 0 else "FFFFFF")
        set_cell_margins(c, 100, 100, 120, 120)
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(9.5)
        if c_i == 0:
            r.font.bold = True
            r.font.color.rgb = COLOR_ORANGE
        elif c_i == 2 and "【終極最大利益】" in text:
            r.font.color.rgb = COLOR_RUST
        else:
            r.font.color.rgb = COLOR_CHARCOAL

# ----------------- CHAPTER 5 -----------------
add_title("第五章：訴訟作戰 SOP 推進甘特時程與家屬檢核表", level=1)

sop_data = [
    ("第一階段（D-Day ~ 2週內）：醫院與證明開立", "帶母親至台中榮總神經內科就醫，同步開妥具備「失智CDR、完全喪失事理辨識、全天需專人照顧」之乙種診斷書，並於區公所領表後於院內完成身心障礙鑑定遞件。"),
    ("第二階段（D+15天 ~ 1個月）：監護宣告與財產清查", "向家事法院送狀聲請對母親做「監護宣告」並指派子女為監護人；持證件前往國稅局調閱父母親雙方全國財產總歸戶清單與近三年綜所稅各類所得資料。"),
    ("第三階段（D+1個月 ~ 2個月）：資產凍結與暫時處分", "由律師向法院聲請「夫妻財產保全處分／假扣押」，凍結父親名下不動產與主要定存；同步聲請「給付家庭生活費與外勞照護費之暫時處分」。"),
    ("第四階段（D+2個月 ~ 6個月）：實體訴訟攻防與談判", "向父親與小三提出侵害配偶權損害賠償訴訟；在家事法庭上運用民法第1052條但書拒絕無理離婚，或反訴主張第1030條之1與第1030條之3追討資產並全面清算。")
]

for title_step, desc_step in sop_data:
    add_title(title_step, level=2)
    add_body_p([(desc_step, False, False)])

# Save Document
doc.save(doc_path)
print("Word docx created successfully at:", doc_path)
