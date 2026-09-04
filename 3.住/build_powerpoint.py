import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUT_DIR = "/Users/howardliao/legal_strategy_project"
prs = Presentation()
prs.slide_width = Inches(13.333) # 16:9
prs.slide_height = Inches(7.5)
blank_slide_layout = prs.slide_layouts[6]

C_WHITE = RGBColor(255, 255, 255)
C_CHARCOAL = RGBColor(45, 55, 72)     # #2D3748 黑灰色
C_ORANGE = RGBColor(222, 88, 20)      # #DE5814 標題橘
C_RUST = RGBColor(168, 50, 18)        # #A83212 鐵鏽
C_AMBER = RGBColor(217, 119, 6)       # #D97706 重點黃金
C_CITRUS = RGBColor(234, 88, 12)      # #EA580C 柑橘
C_LIGHT_BG = RGBColor(255, 251, 235)  # 淺淡琥珀色背景塊 #FFFBEB
FONT_NAME = "PingFang TC"

def add_header(slide, title_text, category_text=""):
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_AMBER
    top_line.line.color.rgb = C_AMBER

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    
    if category_text:
        r_cat = p.add_run()
        r_cat.text = f"【{category_text}】 "
        r_cat.font.name = FONT_NAME
        r_cat.font.size = Pt(14)
        r_cat.font.bold = True
        r_cat.font.color.rgb = C_RUST
        
    r = p.add_run()
    r.text = title_text
    r.font.name = FONT_NAME
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = C_ORANGE

def add_footer(slide):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "八旬失智配偶法律防禦與權益最大化戰略報告 ｜ 報告人：Howard Liao Ph.D.(廖倫豪 博士)"
    r.font.name = FONT_NAME
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(140, 150, 165)

# ----------------- SLIDE 1: COVER -----------------
s1 = prs.slides.add_slide(blank_slide_layout)
bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg.fill.solid()
bg.fill.fore_color.rgb = C_WHITE
bg.line.fill.background()

art_path = os.path.join(OUT_DIR, "pharaoh_cover_art.png")
if os.path.exists(art_path):
    s1.shapes.add_picture(art_path, Inches(6.8), Inches(1.2), width=Inches(5.8))

tb_c = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.0))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

p1 = tf_c.paragraphs[0]
r1 = p1.add_run()
r1.text = "八旬失智配偶法律防禦\n與權益最大化戰略報告\n"
r1.font.name = FONT_NAME
r1.font.size = Pt(32)
r1.font.bold = True
r1.font.color.rgb = C_ORANGE

p2 = tf_c.add_paragraph()
p2.space_before = Pt(10)
r2 = p2.add_run()
r2.text = "阻斷惡意脫產・夫妻剩餘財產清算・監護宣告・追討第三者・照護權益全攻略\n"
r2.font.name = FONT_NAME
r2.font.size = Pt(14)
r2.font.bold = True
r2.font.color.rgb = C_RUST

p3 = tf_c.add_paragraph()
p3.space_before = Pt(24)
r3 = p3.add_run()
r3.text = "報告人：Howard Liao Ph.D.(廖倫豪 博士)\n"
r3.font.name = FONT_NAME
r3.font.size = Pt(16)
r3.font.bold = True
r3.font.color.rgb = C_AMBER

p4 = tf_c.add_paragraph()
p4.space_before = Pt(4)
r4 = p4.add_run()
r4.text = "專案性質：台灣家事法實務戰略與醫療證明指引 ｜ 2026年9月"
r4.font.name = FONT_NAME
r4.font.size = Pt(11)
r4.font.color.rgb = C_CHARCOAL

# ----------------- SLIDE 2: 律師指示——專業醫學與神經學用語 -----------------
s2 = prs.slides.add_slide(blank_slide_layout)
add_header(s2, "診斷書開立指引：律師指示與專業神經醫學用語", "醫療證據")
add_footer(s2)

box1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
box1.fill.solid()
box1.fill.fore_color.rgb = C_LIGHT_BG
box1.line.color.rgb = C_AMBER
box1.line.width = Pt(1.5)

tf1 = box1.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)
p = tf1.paragraphs[0]
r = p.add_run()
r.text = "一、醫院端神經內科「專業醫學用語」"
r.font.name = FONT_NAME
r.font.size = Pt(16)
r.font.bold = True
r.font.color.rgb = C_RUST

items_med = [
    ("非口語「記性差」", "需具體載明「阿茲海默型失智症」或「進行性腦神經退化症」。"),
    ("非單純「退化」", "需載明「嚴重認知功能障礙（Severe Cognitive Impairment）」。"),
    ("定向感障礙", "載明「人、時、地定向感顯著喪失（Disorientation）」。"),
    ("記憶力缺損", "載明「近期與遠期記憶力嚴重缺損，無法回憶重大生活事件」。"),
    ("判斷力喪失", "載明「判斷力、抽象思考與計算能力嚴重衰退」。"),
    ("量表數據指標", "務必載明「臨床失智評估量表（CDR）＝ X分」及 MMSE 測驗分數。")
]
for title_sub, desc_sub in items_med:
    p_sub = tf1.add_paragraph()
    p_sub.space_before = Pt(8)
    r_t = p_sub.add_run()
    r_t.text = f"• {title_sub}："
    r_t.font.name = FONT_NAME
    r_t.font.size = Pt(12)
    r_t.font.bold = True
    r_t.font.color.rgb = C_AMBER
    r_d = p_sub.add_run()
    r_d.text = desc_sub
    r_d.font.name = FONT_NAME
    r_d.font.size = Pt(11)
    r_d.font.color.rgb = C_CHARCOAL

box2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.1))
box2.fill.solid()
box2.fill.fore_color.rgb = C_LIGHT_BG
box2.line.color.rgb = C_ORANGE
box2.line.width = Pt(1.5)

tf2 = box2.text_frame
tf2.word_wrap = True
tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)
p2 = tf2.paragraphs[0]
r2 = p2.add_run()
r2.text = "二、法院審判高度採信之「法定關鍵用語」"
r2.font.name = FONT_NAME
r2.font.size = Pt(16)
r2.font.bold = True
r2.font.color.rgb = C_ORANGE

items_leg = [
    ("意思能力要件", "載明「因精神障礙或心智缺陷，致不能為意思表示或受意思表示，已無處理自己事務之能力」。（民法第14條監護宣告鐵證）"),
    ("阻斷私簽協議", "確認「欠缺完全行為能力與事理辨識能力」，杜絕父親私下誘騙母親簽字離婚或將房產贈與脫產。"),
    ("生活自理依賴", "載明「生活完全無法自理，需專人24小時全天候看護照料」。（爭取高額扶養費與贍養費必備）"),
    ("病程不可逆性", "載明「長期規則於神經內科診療，病況屬永久不可逆神經退化」。（證明母親無過失，駁回對方無理離婚訴請）")
]
for title_sub, desc_sub in items_leg:
    p_sub = tf2.add_paragraph()
    p_sub.space_before = Pt(10)
    r_t = p_sub.add_run()
    r_t.text = f"★ {title_sub}："
    r_t.font.name = FONT_NAME
    r_t.font.size = Pt(12)
    r_t.font.bold = True
    r_t.font.color.rgb = C_AMBER
    r_d = p_sub.add_run()
    r_d.text = desc_sub
    r_d.font.name = FONT_NAME
    r_d.font.size = Pt(11)
    r_d.font.color.rgb = C_CHARCOAL

# ----------------- SLIDE 3: 榮總看診與身心障礙證明 -----------------
s3 = prs.slides.add_slide(blank_slide_layout)
add_header(s3, "台中榮總就診與身心障礙證明（殘障手冊）同步辦理", "醫療與社福")
add_footer(s3)

ankh_path = os.path.join(OUT_DIR, "icon_ankh.png")
if os.path.exists(ankh_path):
    s3.shapes.add_picture(ankh_path, Inches(10.8), Inches(1.8), width=Inches(1.8))

card_w = Inches(9.6)
# Card 1
c1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), card_w, Inches(1.55))
c1.fill.solid()
c1.fill.fore_color.rgb = C_LIGHT_BG
c1.line.color.rgb = C_CITRUS
tfc1 = c1.text_frame
tfc1.word_wrap = True
tfc1.margin_left = tfc1.margin_right = tfc1.margin_top = Inches(0.2)
p = tfc1.paragraphs[0]
r = p.add_run()
r.text = "步驟一：看診前先至戶籍地區公所領取【身心障礙鑑定表】\n"
r.font.bold = True
r.font.size = Pt(14)
r.font.color.rgb = C_RUST
p_sub = tfc1.add_paragraph()
r2 = p_sub.add_run()
r2.text = "攜帶證件：母親身分證正本、印章、1吋照片3張、代辦人身分證與印章。先領取空白表格，避免看診後再度折返。"
r2.font.size = Pt(11)
r2.font.color.rgb = C_CHARCOAL

# Card 2
c2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), card_w, Inches(1.55))
c2.fill.solid()
c2.fill.fore_color.rgb = C_LIGHT_BG
c2.line.color.rgb = C_AMBER
tfc2 = c2.text_frame
tfc2.word_wrap = True
tfc2.margin_left = tfc2.margin_right = tfc2.margin_top = Inches(0.2)
p = tfc2.paragraphs[0]
r = p.add_run()
r.text = "步驟二：門診時交給醫師鑑定填寫，台中榮總院內專人送件\n"
r.font.bold = True
r.font.size = Pt(14)
r.font.color.rgb = C_ORANGE
p_sub = tfc2.add_paragraph()
r2 = p_sub.add_run()
r2.text = "同科其他神經內科醫師可直接調閱田怡婷醫師過去的電腦病歷、腦部影像及量表報告，直接完成生理鑑定；隨後移交第一醫療大樓大廳身障窗口完成生活評估並送件。"
r2.font.size = Pt(11)
r2.font.color.rgb = C_CHARCOAL

# Card 3
c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), card_w, Inches(1.65))
c3.fill.solid()
c3.fill.fore_color.rgb = C_LIGHT_BG
c3.line.color.rgb = C_RUST
tfc3 = c3.text_frame
tfc3.word_wrap = True
tfc3.margin_left = tfc3.margin_right = tfc3.margin_top = Inches(0.2)
p = tfc3.paragraphs[0]
r = p.add_run()
r.text = "取得身心障礙證明之四大實質效益（與外勞資格完全加成）\n"
r.font.bold = True
r.font.size = Pt(14)
r.font.color.rgb = C_RUST
p_sub = tfc3.add_paragraph()
r2 = p_sub.add_run()
r2.text = "1. 綜合所得稅特別扣除額 21.8 萬元/年  2. 健保自付額中度減半、重度全免  3. 專用車輛免徵牌照稅  4. 重度證明免繳外籍看護就業安定費（省 2,000元/月）。"
r2.font.size = Pt(11)
r2.font.color.rgb = C_CHARCOAL

# ----------------- SLIDE 4: 第一階段——緊急防禦與止血 -----------------
s4 = prs.slides.add_slide(blank_slide_layout)
add_header(s4, "第一階段：緊急法律防禦——監護宣告與財產凍結", "防禦止血")
add_footer(s4)

eye_path = os.path.join(OUT_DIR, "icon_eye_horus.png")
if os.path.exists(eye_path):
    s4.shapes.add_picture(eye_path, Inches(11.0), Inches(0.6), width=Inches(1.5))

col_w = Inches(3.7)
col_h = Inches(5.0)

# Col 1
b1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), col_w, col_h)
b1.fill.solid()
b1.fill.fore_color.rgb = C_LIGHT_BG
b1.line.color.rgb = C_ORANGE
b1.line.width = Pt(1.5)
tfb1 = b1.text_frame
tfb1.word_wrap = True
tfb1.margin_left = tfb1.margin_right = tfb1.margin_top = Inches(0.25)
p = tfb1.paragraphs[0]
r = p.add_run()
r.text = "1. 聲請「監護宣告」\n指派子女為法定監護人\n"
r.font.size = Pt(15)
r.font.bold = True
r.font.color.rgb = C_ORANGE
bullet_1 = [
    ("隔離父親操控", "母親已無法表達法律意志，由子女擔任法定代理人，阻絕任何私下簽署之風險。"),
    ("法定訴訟代理", "在後續所有離婚、分產官司中，均由監護人代表母親出庭捍衛權益。"),
    ("資產安全鎖定", "母親名下存摺、印鑑、房地產全數納入家事法院監管保護。")
]
for bt, bd in bullet_1:
    p_b = tfb1.add_paragraph()
    p_b.space_before = Pt(8)
    r_t = p_b.add_run()
    r_t.text = f"• {bt}："
    r_t.font.bold = True
    r_t.font.size = Pt(11.5)
    r_t.font.color.rgb = C_AMBER
    r_d = p_b.add_run()
    r_d.text = bd
    r_d.font.size = Pt(10.5)
    r_d.font.color.rgb = C_CHARCOAL

# Col 2
b2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.6), col_w, col_h)
b2.fill.solid()
b2.fill.fore_color.rgb = C_LIGHT_BG
b2.line.color.rgb = C_RUST
b2.line.width = Pt(1.5)
tfb2 = b2.text_frame
tfb2.word_wrap = True
tfb2.margin_left = tfb2.margin_right = tfb2.margin_top = Inches(0.25)
p = tfb2.paragraphs[0]
r = p.add_run()
r.text = "2. 調閱國稅局清單\n全面清查父親資產底牌\n"
r.font.size = Pt(15)
r.font.bold = True
r.font.color.rgb = C_RUST
bullet_2 = [
    ("全國財產總歸戶", "調閱父親名下全部不動產（地號、建號、持分比例與公告現值）。"),
    ("近三年綜所稅清單", "查明大額銀行存款（從利息所得反推本金）及上市櫃股票股利明細。"),
    ("鎖定資產基數", "迅速掌握父親總身價，作為日後剩餘財產清算平分之法庭鐵證。")
]
for bt, bd in bullet_2:
    p_b = tfb2.add_paragraph()
    p_b.space_before = Pt(8)
    r_t = p_b.add_run()
    r_t.text = f"• {bt}："
    r_t.font.bold = True
    r_t.font.size = Pt(11.5)
    r_t.font.color.rgb = C_AMBER
    r_d = p_b.add_run()
    r_d.text = bd
    r_d.font.size = Pt(10.5)
    r_d.font.color.rgb = C_CHARCOAL

# Col 3
b3 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.6), col_w, col_h)
b3.fill.solid()
b3.fill.fore_color.rgb = C_LIGHT_BG
b3.line.color.rgb = C_CITRUS
b3.line.width = Pt(1.5)
tfb3 = b3.text_frame
tfb3.word_wrap = True
tfb3.margin_left = tfb3.margin_right = tfb3.margin_top = Inches(0.25)
p = tfb3.paragraphs[0]
r = p.add_run()
r.text = "3. 假扣押與暫時處分\n阻斷資產洗錢給小三\n"
r.font.size = Pt(15)
r.font.bold = True
r.font.color.rgb = C_CITRUS
bullet_3 = [
    ("財產保全假扣押", "查封凍結父親主要房產與高額銀行存款，禁止買賣、移轉或設定抵押。"),
    ("暫時處分扣生活費", "強制裁定父親在訴訟期間，按月支付母親外籍看護薪資與醫療開銷。"),
    ("破解惡意脫產", "即時凍結現場，防止父親藉由假借貸、轉帳、買車買房贈與第三者。")
]
for bt, bd in bullet_3:
    p_b = tfb3.add_paragraph()
    p_b.space_before = Pt(8)
    r_t = p_b.add_run()
    r_t.text = f"• {bt}："
    r_t.font.bold = True
    r_t.font.size = Pt(11.5)
    r_t.font.color.rgb = C_AMBER
    r_d = p_b.add_run()
    r_d.text = bd
    r_d.font.size = Pt(10.5)
    r_d.font.color.rgb = C_CHARCOAL

# ----------------- SLIDE 5: 第二階段——四大金錢請求最大化 -----------------
s5 = prs.slides.add_slide(blank_slide_layout)
add_header(s5, "第二階段：爭取母親權益最大化——四大核心金錢請求", "訴訟求償")
add_footer(s5)

scale_path = os.path.join(OUT_DIR, "icon_scales.png")
if os.path.exists(scale_path):
    s5.shapes.add_picture(scale_path, Inches(11.2), Inches(0.5), width=Inches(1.5))

table_shape = s5.shapes.add_table(5, 4, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
tbl = table_shape.table
tbl.columns[0].width = Inches(2.2)
tbl.columns[1].width = Inches(2.4)
tbl.columns[2].width = Inches(4.3)
tbl.columns[3].width = Inches(2.833)

headers = ["求償項目", "法定依據", "求償內涵與法理策略", "預估效益與實戰定位"]
for idx, h in enumerate(headers):
    cell = tbl.cell(0, idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(254, 243, 199)
    p = cell.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = h
    r.font.name = FONT_NAME
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = C_RUST

claims_data = [
    ("夫妻剩餘財產分配", "民法第 1030 條之 1", "清查雙方婚後增加財產淨額，扣除負債後差額平均分配。八十歲累積房產與存款多屬婚後所得，母親依法分得一半。", "【金額最大宗・佔90%以上】\n數百萬至數千萬元不等之法定產權。"),
    ("追討第三者條款", "民法第 1030 條之 3\n民法第 1020 條之 1", "起訴前五年內，父親為減少分配而惡意贈與第三者之資產，全數「追加計算」為婚後財產！一年內無償贈與可直接訴請撤銷。", "【防止暗渡陳倉殺手鐧】\n轉移給小三的現金房產全數追回計入。"),
    ("侵害配偶權賠償", "民法第 184 條\n民法第 195 條第 3 項", "將父親與小三列為連帶共同被告。舉證兩人親密交往破壞婚姻，審酌原配重病遭背叛之重大痛苦，判令連帶賠償精神慰撫金。", "【直擊小三連帶賠償】\n實務判賠約 30萬 ～ 100萬元。"),
    ("判決離婚賠償\n與終身照護贍養費", "民法第 1056 條\n民法第 1057 條", "因可歸責父親事由致判決離婚之非財產損害；加計母親失智重症無謀生能力，判命按月或一次性給付外勞、醫療照護全額贍養費。", "【保障晚年尊嚴】\n外勞薪資+照護耗材，每月全額強制給付。")
]

for row_i, (c0, c1, c2, c3) in enumerate(claims_data, start=1):
    for col_i, text in enumerate([c0, c1, c2, c3]):
        cell = tbl.cell(row_i, col_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_i % 2 == 1 else RGBColor(255, 253, 247)
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = text
        r.font.name = FONT_NAME
        r.font.size = Pt(10.5)
        if col_i == 0:
            r.font.bold = True
            r.font.color.rgb = C_ORANGE
        elif col_i == 3:
            r.font.bold = True
            r.font.color.rgb = C_RUST
        else:
            r.font.color.rgb = C_CHARCOAL

# ----------------- SLIDE 6: 戰略抉擇——離 vs 不離 -----------------
s6 = prs.slides.add_slide(blank_slide_layout)
add_header(s6, "核心戰略博弈：八旬長輩「離」與「不離」的極限抉擇", "戰略決策")
add_footer(s6)

b_a = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
b_a.fill.solid()
b_a.fill.fore_color.rgb = C_LIGHT_BG
b_a.line.color.rgb = C_RUST
b_a.line.width = Pt(2)
tfa = b_a.text_frame
tfa.word_wrap = True
tfa.margin_left = tfa.margin_right = tfa.margin_top = Inches(0.3)
p = tfa.paragraphs[0]
r = p.add_run()
r.text = "策略 A：堅決不離（以拖待變・遺產保全）\n"
r.font.size = Pt(17)
r.font.bold = True
r.font.color.rgb = C_RUST

items_a = [
    ("法律防線極度堅固", "依民法第1052條第2項但書，外遇過失方無權強逼無過失生病原配離婚。法院極度排斥丟包病妻，判離機率極低。"),
    ("聲請強制生活費給付", "向法院聲請暫時處分，要求父親按月給付外籍看護費用與生活費，經濟無虞。"),
    ("【最大利益：合法繼承權】", "母親保有配偶第一順位法定繼承權！父親百年時，母親先拿剩餘財產一半，再與子女均分剩餘遺產。小三為法律局外人，一毛都分不到！")
]
for at, ad in items_a:
    pa = tfa.add_paragraph()
    pa.space_before = Pt(10)
    ra_t = pa.add_run()
    ra_t.text = f"★ {at}：\n"
    ra_t.font.bold = True
    ra_t.font.size = Pt(11.5)
    ra_t.font.color.rgb = C_AMBER
    ra_d = pa.add_run()
    ra_d.text = ad
    ra_d.font.size = Pt(10.5)
    ra_d.font.color.rgb = C_CHARCOAL

b_b = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.1))
b_b.fill.solid()
b_b.fill.fore_color.rgb = C_LIGHT_BG
b_b.line.color.rgb = C_ORANGE
b_b.line.width = Pt(2)
tfb = b_b.text_frame
tfb.word_wrap = True
tfb.margin_left = tfb.margin_right = tfb.margin_top = Inches(0.3)
p = tfb.paragraphs[0]
r = p.add_run()
r.text = "策略 B：反訴離婚（即刻落袋・徹底切割）\n"
r.font.size = Pt(17)
r.font.bold = True
r.font.color.rgb = C_ORANGE

items_b = [
    ("啟動時機", "發現父親正急速變賣房產、解約大額定存、密集贈與洗錢給小三，拖延恐遭掏空資產時採用。"),
    ("閃電強制假扣押", "立刻向法院反訴離婚，全面聲請假扣押查封其所有已知不動產與銀行帳戶。"),
    ("【最大利益：落袋為安信託】", "依判決強制執行將數千萬產權與存款平分登記至母親名下。由監護人設立「高齡安養信託」，確保母親醫療與照護安享晚年。")
]
for bt, bd in items_b:
    pb = tfb.add_paragraph()
    pb.space_before = Pt(10)
    rb_t = pb.add_run()
    rb_t.text = f"★ {bt}：\n"
    rb_t.font.bold = True
    rb_t.font.size = Pt(11.5)
    rb_t.font.color.rgb = C_AMBER
    rb_d = pb.add_run()
    rb_d.text = bd
    rb_d.font.size = Pt(10.5)
    rb_d.font.color.rgb = C_CHARCOAL

# ----------------- SLIDE 7: 執行 SOP 與時程推進 -----------------
s7 = prs.slides.add_slide(blank_slide_layout)
add_header(s7, "實戰執行 SOP 推進時程與家屬行動檢核", "行動時程")
add_footer(s7)

pyr_path = os.path.join(OUT_DIR, "icon_pyramid.png")
if os.path.exists(pyr_path):
    s7.shapes.add_picture(pyr_path, Inches(11.2), Inches(0.5), width=Inches(1.5))

steps = [
    ("第一階段（即刻~2週內）", "醫院鑑定與證明開立", "帶母親至台中榮總神經內科就醫；同步開妥載明「CDR失智、無辨識意思能力、24小時專人看護」之訴訟診斷書；攜帶公所表格完成身心障礙鑑定遞件。"),
    ("第二階段（第2~4週）", "監護宣告與財產清查", "向家事法院具狀聲請「監護宣告」指派子女為監護人；向國稅局調閱父母雙方全國財產總歸戶清單及近三年綜所稅各類所得資料，徹底摸清資產底牌。"),
    ("第三階段（第1~2個月）", "資產凍結與暫時處分", "由委任律師向法院聲請「夫妻財產保全處分／假扣押」，全面凍結父親名下不動產與定存；聲請暫時處分強制父親按月匯給外勞薪資與生活照料費。"),
    ("第四階段（第2~6個月）", "實體法庭反擊與求償", "連帶控告父親與小三侵害配偶權（求償百萬）；在家事法庭以民法第1052條但書阻斷惡意離婚，或發動民法第1030-1剩餘財產平分與第1030-3追討小三全數資產。")
]

step_top = 1.6
for s_phase, s_title, s_desc in steps:
    card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(step_top), Inches(10.2), Inches(1.15))
    card.fill.solid()
    card.fill.fore_color.rgb = C_LIGHT_BG
    card.line.color.rgb = C_AMBER
    card.line.width = Pt(1)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.18)
    
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = f"【{s_phase}】 {s_title}： "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = C_ORANGE
    
    r2 = p.add_run()
    r2.text = s_desc
    r2.font.name = FONT_NAME
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_CHARCOAL
    
    step_top += 1.3

pptx_path = os.path.join(OUT_DIR, "legal_strategy_presentation.pptx")
prs.save(pptx_path)
print("PowerPoint created successfully at:", pptx_path)
