import re

with open('templates/social_media_interactive.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The top part of the file up to the start of the first Real-Life Situation block
top_marker = '    <!-- ═══════════════════════════════════════════════════════════ -->\n    <!-- 0. REAL-LIFE SITUATION SECTION — Immersive Crime-Specific  -->'
top_idx = content.find(top_marker)

# The hero section which marks the end of all the real-life situation duplicates
bottom_marker = '    <!-- ═══════════════════════════════════════════════════════════ -->\n    <!-- 1. Hero / Title Section -->'
bottom_idx = content.rfind(bottom_marker)

if top_idx == -1 or bottom_idx == -1:
    print("Markers not found!")
    import sys
    sys.exit(1)

top_content = content[:top_idx]
bottom_content = content[bottom_idx:]

# The correct real-life situation block wrapped in if crime_id != 'csam'
correct_block = r'''    {% if crime_id != 'csam' %}
    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- 0. REAL-LIFE SITUATION SECTION — Immersive Crime-Specific  -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section id="real-life-section" style="margin-bottom: 48px; position: relative;">

        <!-- Section Badge -->
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 22px; flex-wrap: wrap;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(135deg,#4CAF50,#2e7d32); border-radius: 30px; padding: 8px 20px; box-shadow: 0 4px 14px rgba(76,175,80,0.35);">
                <i class="fa-solid fa-film" style="color:#fff; font-size:0.85rem;"></i>
                <span style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; color:#fff;">Real-Life Situation</span>
            </div>
            <div style="height:2px; flex:1; background:linear-gradient(90deg,rgba(76,175,80,0.35),transparent); border-radius:2px;"></div>
        </div>

        <div style="background:var(--white); border-radius:20px; border:1px solid rgba(101,146,135,0.15); box-shadow:0 8px 40px rgba(0,0,0,0.07); overflow:hidden; position:relative;">

            <!-- Intro Header -->
            <div style="padding:28px 32px 0 32px;">
                <h3 style="font-size:1.5rem; color:var(--dark-text); margin-bottom:6px;">How Does This Actually Happen?</h3>
                <p style="font-size:0.95rem; color:var(--light-text); line-height:1.6; margin-bottom:24px;">Step into this realistic situation and experience what a real victim encounters. Read every message carefully — then decide what the right action is.</p>
            </div>

            <!-- ─────────────────────────────────────────── -->
            {# ── Sexually Explicit: Instagram DM UI ── #}
            {% if crime_id == 'sexually-explicit' %}
            <div style="padding:0 32px 32px 32px;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start;">

                    <!-- Instagram DM Clone -->
                    <div style="border-radius:18px;overflow:hidden;box-shadow:0 8px 35px rgba(0,0,0,0.2);background:#fff;border:1px solid #dbdbdb;">
                        <!-- IG Header -->
                        <div style="background:linear-gradient(90deg,#f58529,#dd2a7b,#8134af,#515bd4);padding:2px;">
                            <div style="background:#fff;margin:0;padding:0;">
                                <div style="padding:12px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #efefef;">
                                    <i class="fa-solid fa-arrow-left" style="color:#262626;font-size:0.9rem;"></i>
                                    <div style="position:relative;flex-shrink:0;">
                                        <div style="width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#f58529,#dd2a7b,#8134af);padding:2px;">
                                            <div style="width:100%;height:100%;border-radius:50%;background:#eee;display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:800;color:#8134af;">A</div>
                                        </div>
                                        <div style="position:absolute;bottom:0;right:0;width:11px;height:11px;border-radius:50%;background:#4CAF50;border:2px solid white;"></div>
                                    </div>
                                    <div style="flex:1;">
                                        <div style="font-size:0.88rem;font-weight:700;color:#262626;">alex_photo_studio</div>
                                        <div style="font-size:0.7rem;color:#8e8e8e;">Active now</div>
                                    </div>
                                    <i class="fa-solid fa-phone" style="color:#262626;font-size:0.9rem;"></i>
                                    <i class="fa-solid fa-video" style="color:#262626;font-size:0.9rem;margin-left:10px;"></i>
                                </div>
                            </div>
                        </div>

                        <!-- Chat body -->
                        <div style="background:#fafafa;padding:16px 12px;display:flex;flex-direction:column;gap:12px;height:240px;overflow-y:auto;">
                            <div style="text-align:center;font-size:0.65rem;color:#8e8e8e;margin-bottom:8px;">8:42 PM</div>
                            
                            <!-- Received msg 1 -->
                            <div style="display:flex;align-items:flex-end;gap:8px;">
                                <div style="width:24px;height:24px;border-radius:50%;background:#eee;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:800;color:#8134af;flex-shrink:0;">A</div>
                                <div style="background:#efefef;color:#262626;padding:10px 14px;border-radius:18px 18px 18px 4px;font-size:0.82rem;line-height:1.4;max-width:80%;">
                                    Hi! I came across your profile and honestly you have a really unique look 📸 I work with a media agency and we're scouting fresh faces.
                                </div>
                            </div>
                            
                            <!-- Received msg 2 -->
                            <div style="display:flex;align-items:flex-end;gap:8px;">
                                <div style="width:24px;height:24px;border-radius:50%;background:#eee;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:800;color:#8134af;flex-shrink:0;opacity:0;">A</div>
                                <div style="background:#efefef;color:#262626;padding:10px 14px;border-radius:4px 18px 18px 18px;font-size:0.82rem;line-height:1.4;max-width:80%;">
                                    It's for a paid campaign — ₹8,000/day, totally confidential. We've worked with 200+ models. Interested? 🌟
                                </div>
                            </div>

                            <!-- Sent msg (You) -->
                            <div style="display:flex;align-items:flex-end;justify-content:flex-end;gap:8px;">
                                <div style="background:linear-gradient(135deg,#8134af,#dd2a7b);color:white;padding:10px 14px;border-radius:18px 18px 4px 18px;font-size:0.82rem;line-height:1.4;max-width:80%;">
                                    Oh wow, really? I've never modelled before though. What exactly do you need?
                                </div>
                            </div>

                            <!-- Received msg 3 (The Trap) -->
                            <div style="display:flex;align-items:flex-end;gap:8px;">
                                <div style="width:24px;height:24px;border-radius:50%;background:#eee;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:800;color:#8134af;flex-shrink:0;">A</div>
                                <div style="background:rgba(221,42,123,0.1);border:1px solid rgba(221,42,123,0.3);color:#262626;padding:10px 14px;border-radius:18px 18px 18px 4px;font-size:0.82rem;line-height:1.4;max-width:80%;">
                                    To shortlist you officially, I just need a few private reference photos sent here first. Our panel reviews them confidentially. 🔒 Don't worry, it's standard procedure.
                                </div>
                            </div>
                        </div>

                        <!-- IG Input area -->
                        <div style="padding:10px 14px;background:#fff;border-top:1px solid #efefef;display:flex;align-items:center;gap:12px;">
                            <div style="width:34px;height:34px;border-radius:50%;background:#0095f6;display:flex;align-items:center;justify-content:center;color:white;flex-shrink:0;"><i class="fa-solid fa-camera"></i></div>
                            <div style="flex:1;background:#efefef;border-radius:20px;padding:8px 14px;font-size:0.82rem;color:#8e8e8e;display:flex;align-items:center;justify-content:space-between;">
                                <span>Message...</span>
                                <div style="display:flex;gap:12px;"><i class="fa-solid fa-microphone"></i><i class="fa-regular fa-image"></i><i class="fa-regular fa-face-smile"></i></div>
                            </div>
                        </div>
                    </div>

                    <!-- IG Decision Panel -->
                    <div style="display:flex;flex-direction:column;gap:18px;">
                        <div style="background:rgba(221,42,123,0.06);border:1px solid rgba(221,42,123,0.2);border-radius:12px;padding:16px;">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                <i class="fa-solid fa-triangle-exclamation" style="color:#dd2a7b;"></i>
                                <span style="font-weight:700;font-size:0.9rem;color:#dd2a7b;">Crucial Moment</span>
                            </div>
                            <p style="font-size:0.9rem;color:var(--dark-text);line-height:1.6;margin:0;">{{ crime.real_situation.decision_prompt }}</p>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:10px;" id="situation-options">
                            {% for opt in crime.real_situation.decision_options %}
                            <button class="option-btn situation-choice-btn" data-correct="{{ 'true' if opt.correct else 'false' }}" data-feedback="{{ opt.feedback }}" onclick="handleSituationChoice(this)" style="width:100%;text-align:left;padding:14px 18px;font-size:0.92rem;border-radius:10px;display:flex;align-items:flex-start;gap:10px;line-height:1.4;border:1px solid rgba(221,42,123,0.25);background:var(--white);cursor:pointer;transition:all 0.2s;font-family:inherit;">
                                <i class="fa-solid fa-chevron-right" style="color:#dd2a7b;margin-top:3px;flex-shrink:0;"></i>
                                <span>{{ opt.label }}</span>
                            </button>
                            {% endfor %}
                        </div>
                        <div id="situation-feedback" style="display:none;padding:16px 20px;border-radius:10px;font-size:0.9rem;line-height:1.5;animation:slideDownFade 0.4s ease both;"></div>
                    </div>
                </div>
            </div>

            {# ── Obscene Content: WhatsApp UI ── #}
            {% elif crime_id == 'obscene-content' %}
            <div style="padding:0 32px 32px 32px;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start;">

                    <!-- WhatsApp Clone -->
                    <div style="border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.15);background:#efeae2;border:1px solid #d1d7db;position:relative;">
                        <!-- WhatsApp Header -->
                        <div style="background:#00a884;padding:12px 16px;display:flex;align-items:center;gap:12px;color:white;">
                            <i class="fa-solid fa-arrow-left" style="font-size:1.1rem;"></i>
                            <div style="width:38px;height:38px;border-radius:50%;background:#dfe5e7;display:flex;align-items:center;justify-content:center;color:#54656f;font-size:1.2rem;overflow:hidden;">
                                <i class="fa-solid fa-users"></i>
                            </div>
                            <div style="flex:1;">
                                <div style="font-size:0.95rem;font-weight:600;margin-bottom:2px;">College Gang 🔥</div>
                                <div style="font-size:0.7rem;opacity:0.9;">Arjun, Neha, Rahul, You</div>
                            </div>
                            <i class="fa-solid fa-video" style="font-size:1.1rem;"></i>
                            <i class="fa-solid fa-phone" style="font-size:1.1rem;margin:0 8px;"></i>
                            <i class="fa-solid fa-ellipsis-vertical" style="font-size:1.2rem;"></i>
                        </div>

                        <!-- WhatsApp Body -->
                        <div style="padding:16px;display:flex;flex-direction:column;gap:8px;height:260px;overflow-y:auto;background-image:url('data:image/svg+xml;utf8,<svg width=\"100\" height=\"100\" xmlns=\"http://www.w3.org/2000/svg\"><g fill=\"none\" stroke=\"%23d1d7db\" stroke-width=\"1\" opacity=\"0.2\"><path d=\"M10,10 L30,30 M50,10 L70,30 M90,10 L10,30\"/></g></svg>');">
                            <div style="background:#fff;align-self:center;padding:4px 12px;border-radius:8px;font-size:0.7rem;color:#54656f;box-shadow:0 1px 2px rgba(0,0,0,0.08);margin-bottom:8px;">TODAY</div>
                            
                            <!-- Arjun Msg -->
                            <div style="align-self:flex-start;background:#fff;padding:6px 8px 6px 12px;border-radius:0 8px 8px 8px;max-width:85%;box-shadow:0 1px 1px rgba(0,0,0,0.1);position:relative;">
                                <div style="font-size:0.75rem;font-weight:700;color:#e17055;margin-bottom:2px;">Arjun S</div>
                                <div style="font-size:0.85rem;color:#111;line-height:1.4;">Guys 😂😂 got this from a Telegram channel. Going absolutely viral rn 🔥</div>
                                <div style="text-align:right;font-size:0.65rem;color:#667781;margin-top:2px;">2:14 PM</div>
                            </div>
                            
                            <!-- Arjun Attachment -->
                            <div style="align-self:flex-start;background:#fff;padding:4px;border-radius:8px;max-width:85%;box-shadow:0 1px 1px rgba(0,0,0,0.1);">
                                <div style="font-size:0.75rem;font-weight:700;color:#e17055;margin:4px 8px 6px 8px;">Arjun S</div>
                                <div style="background:#f5f5f5;border-radius:6px;width:200px;height:120px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;">
                                    <i class="fa-solid fa-play" style="color:white;font-size:2rem;z-index:2;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.3));"></i>
                                    <div style="position:absolute;bottom:6px;left:6px;background:rgba(0,0,0,0.6);color:white;padding:2px 6px;border-radius:10px;font-size:0.65rem;">0:45</div>
                                </div>
                                <div style="padding:6px 4px 2px;">
                                    <div style="font-size:0.75rem;color:#111;margin-bottom:4px;font-weight:600;"><i class="fa-solid fa-share" style="color:#667781;font-size:0.65rem;margin-right:4px;"></i>Forwarded many times</div>
                                    <div style="text-align:right;font-size:0.65rem;color:#667781;">2:14 PM</div>
                                </div>
                            </div>
                            
                            <!-- Neha Msg -->
                            <div style="align-self:flex-start;background:#fff;padding:6px 8px 6px 12px;border-radius:8px;max-width:85%;box-shadow:0 1px 1px rgba(0,0,0,0.1);">
                                <div style="font-size:0.75rem;font-weight:700;color:#d63031;margin-bottom:2px;">Neha T</div>
                                <div style="font-size:0.85rem;color:#111;line-height:1.4;">OMG 💀 forward this to the hostel group NOW everyone needs to see this 😭😭</div>
                                <div style="text-align:right;font-size:0.65rem;color:#667781;margin-top:2px;">2:16 PM</div>
                            </div>
                            
                            <!-- Arjun Msg 2 (Pressure) -->
                            <div style="align-self:flex-start;background:#fff;border:1px solid rgba(225,112,85,0.4);padding:6px 8px 6px 12px;border-radius:8px;max-width:85%;box-shadow:0 1px 1px rgba(0,0,0,0.1);">
                                <div style="font-size:0.75rem;font-weight:700;color:#e17055;margin-bottom:2px;">Arjun S</div>
                                <div style="font-size:0.85rem;color:#111;line-height:1.4;">don't be a killjoy yaar 🙄 it's harmless fun, everyone in all college groups is doing it. If you don't forward it you're boring 😏</div>
                                <div style="text-align:right;font-size:0.65rem;color:#667781;margin-top:2px;">2:18 PM</div>
                            </div>
                        </div>

                        <!-- Input -->
                        <div style="padding:10px;background:#f0f2f5;display:flex;align-items:center;gap:10px;">
                            <div style="width:36px;height:36px;display:flex;align-items:center;justify-content:center;color:#54656f;font-size:1.2rem;"><i class="fa-regular fa-face-smile"></i></div>
                            <div style="flex:1;background:#fff;border-radius:24px;padding:10px 16px;font-size:0.9rem;color:#8696a0;display:flex;justify-content:space-between;">
                                Message
                                <i class="fa-solid fa-paperclip"></i>
                            </div>
                            <div style="width:40px;height:40px;border-radius:50%;background:#00a884;display:flex;align-items:center;justify-content:center;color:white;"><i class="fa-solid fa-microphone"></i></div>
                        </div>
                    </div>

                    <!-- WhatsApp Decision Panel -->
                    <div style="display:flex;flex-direction:column;gap:18px;">
                        <div style="background:rgba(37,211,102,0.08);border:1px solid rgba(37,211,102,0.3);border-radius:12px;padding:16px;">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                <i class="fa-solid fa-triangle-exclamation" style="color:#1da851;"></i>
                                <span style="font-weight:700;font-size:0.9rem;color:#1da851;">Peer Pressure Alert</span>
                            </div>
                            <p style="font-size:0.9rem;color:var(--dark-text);line-height:1.6;margin:0;">{{ crime.real_situation.decision_prompt }}</p>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:10px;" id="situation-options">
                            {% for opt in crime.real_situation.decision_options %}
                            <button class="option-btn situation-choice-btn" data-correct="{{ 'true' if opt.correct else 'false' }}" data-feedback="{{ opt.feedback }}" onclick="handleSituationChoice(this)" style="width:100%;text-align:left;padding:14px 18px;font-size:0.92rem;border-radius:10px;display:flex;align-items:flex-start;gap:10px;line-height:1.4;border:1px solid rgba(37,211,102,0.3);background:var(--white);cursor:pointer;transition:all 0.2s;font-family:inherit;">
                                <i class="fa-solid fa-check" style="color:#25d366;margin-top:3px;flex-shrink:0;"></i>
                                <span>{{ opt.label }}</span>
                            </button>
                            {% endfor %}
                        </div>
                        <div id="situation-feedback" style="display:none;padding:16px 20px;border-radius:10px;font-size:0.9rem;line-height:1.5;animation:slideDownFade 0.4s ease both;"></div>
                    </div>
                </div>
            </div>

            {# ── Fallback / Fake Accounts: General Message UI ── #}
            {% else %}
            <div style="padding:0 32px 32px 32px;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start;">

                    <!-- Messenger Clone -->
                    <div style="border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.15);background:#fff;border:1px solid #e4e6eb;">
                        <!-- Header -->
                        <div style="background:#fff;padding:12px 16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #e4e6eb;box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                            <i class="fa-solid fa-arrow-left" style="font-size:1.1rem;color:#050505;"></i>
                            <div style="width:36px;height:36px;border-radius:50%;background:#e4e6eb;display:flex;align-items:center;justify-content:center;color:#050505;font-weight:700;">S</div>
                            <div style="flex:1;">
                                <div style="font-size:0.95rem;font-weight:600;color:#050505;margin-bottom:2px;">Sunita Sharma</div>
                                <div style="font-size:0.7rem;color:#65676b;">Active now</div>
                            </div>
                            <i class="fa-solid fa-phone" style="font-size:1.1rem;color:#0084ff;"></i>
                            <i class="fa-solid fa-video" style="font-size:1.1rem;color:#0084ff;margin:0 8px;"></i>
                        </div>

                        <!-- Body -->
                        <div style="padding:16px;display:flex;flex-direction:column;gap:12px;height:240px;overflow-y:auto;background:#f0f0f0;">
                            <div style="text-align:center;font-size:0.7rem;color:#65676b;margin-bottom:10px;">AUG 12, 10:42 AM</div>
                            
                            <div style="text-align:center;background:rgba(0,0,0,0.04);border-radius:10px;padding:8px 12px;font-size:0.75rem;color:#65676b;margin-bottom:8px;align-self:center;">
                                Sunita Sharma is not on your friends list.<br>Account created 2 days ago.
                            </div>

                            <div style="display:flex;align-items:flex-end;gap:8px;max-width:85%;">
                                <div style="width:28px;height:28px;border-radius:50%;background:#e4e6eb;display:flex;align-items:center;justify-content:center;color:#050505;font-weight:700;font-size:0.7rem;flex-shrink:0;">S</div>
                                <div style="background:#e4e6eb;color:#050505;padding:10px 14px;border-radius:18px 18px 18px 4px;font-size:0.85rem;line-height:1.4;">
                                    Hello beta! 🙏 I'm Sunita Aunty, your neighbour from D-block. I've made a new Facebook because my old one got hacked. Please add me on this one too!
                                </div>
                            </div>

                            <div style="display:flex;align-items:flex-end;gap:8px;max-width:85%;">
                                <div style="width:28px;height:28px;border-radius:50%;background:#e4e6eb;display:flex;align-items:center;justify-content:center;color:#050505;font-weight:700;font-size:0.7rem;flex-shrink:0;">S</div>
                                <div style="background:#e4e6eb;color:#050505;padding:10px 14px;border-radius:4px 18px 18px 18px;font-size:0.85rem;line-height:1.4;">
                                    Beta I'm in a very urgent situation 🙏 I'm at the hospital right now with my daughter. I forgot my wallet at home and I need ₹3,000 immediately for her medicines.
                                </div>
                            </div>
                            
                            <div style="display:flex;align-items:flex-end;gap:8px;max-width:85%;">
                                <div style="width:28px;height:28px;border-radius:50%;background:#e4e6eb;display:flex;align-items:center;justify-content:center;color:#050505;font-weight:700;font-size:0.7rem;flex-shrink:0;">S</div>
                                <div style="background:rgba(220,53,69,0.1);border:1px solid rgba(220,53,69,0.3);color:#050505;padding:10px 14px;border-radius:4px 18px 18px 18px;font-size:0.85rem;line-height:1.4;">
                                    Please send it to this UPI: sunita.help2024@paytm — I will return it tonight. And beta please don't tell my husband yet, he'll panic 🙏🙏
                                </div>
                            </div>
                        </div>

                        <!-- Input -->
                        <div style="padding:10px 14px;background:#fff;display:flex;align-items:center;gap:12px;border-top:1px solid #e4e6eb;">
                            <i class="fa-solid fa-circle-plus" style="color:#0084ff;font-size:1.2rem;"></i>
                            <div style="flex:1;background:#f0f2f5;border-radius:20px;padding:8px 14px;font-size:0.85rem;color:#65676b;display:flex;justify-content:space-between;align-items:center;">
                                Aa
                                <i class="fa-regular fa-face-smile" style="color:#0084ff;"></i>
                            </div>
                            <i class="fa-solid fa-thumbs-up" style="color:#0084ff;font-size:1.2rem;"></i>
                        </div>
                    </div>

                    <!-- Messenger Decision Panel -->
                    <div style="display:flex;flex-direction:column;gap:18px;">
                        <div style="background:rgba(0,132,255,0.06);border:1px solid rgba(0,132,255,0.2);border-radius:12px;padding:16px;">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                <i class="fa-solid fa-triangle-exclamation" style="color:#0084ff;"></i>
                                <span style="font-weight:700;font-size:0.9rem;color:#0084ff;">Urgency Warning</span>
                            </div>
                            <p style="font-size:0.9rem;color:var(--light-text);line-height:1.6;margin:0;">{{ crime.real_situation.decision_prompt }}</p>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:12px;" id="situation-options">
                            {% for opt in crime.real_situation.decision_options %}
                            <button class="option-btn situation-choice-btn" data-correct="{{ 'true' if opt.correct else 'false' }}" data-feedback="{{ opt.feedback }}" onclick="handleSituationChoice(this)" style="width:100%;text-align:left;padding:14px 18px;font-size:0.92rem;border-radius:10px;display:flex;align-items:flex-start;gap:10px;line-height:1.4;border:1px solid rgba(101,146,135,0.2);background:var(--white);cursor:pointer;transition:all 0.2s;font-family:inherit;">
                                <i class="fa-solid fa-circle-dot" style="color:var(--primary-color);margin-top:3px;flex-shrink:0;"></i>
                                <span>{{ opt.label }}</span>
                            </button>
                            {% endfor %}
                        </div>
                        <div id="situation-feedback" style="display:none;padding:16px 20px;border-radius:10px;font-size:0.9rem;line-height:1.5;animation:slideDownFade 0.4s ease both;"></div>
                    </div>
                </div>
            </div>
            {% endif %}

        </div><!-- end card -->
    </section>
    {% endif %}
'''

new_content = top_content + correct_block + '\n' + bottom_content

with open('templates/social_media_interactive.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("HTML Fixed!")
