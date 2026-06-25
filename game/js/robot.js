// ════════════════════════════════════════════════════
//  robot.js — Robot 基类
//  提供所有机器人的公共属性和序列化接口。
//  具体机器人类型（侦察、防御、医疗等）应继承此类。
// ════════════════════════════════════════════════════

class Robot {

  /**
   * @param {Object} options
   * @param {number}  options.volume      - 体积（m³）
   * @param {boolean} options.movable     - 是否可移动
   * @param {number}  options.speed       - 移动速度（m/s）
   * @param {number}  options.energyCost  - 耗能（W）
   * @param {string[]} options.skills     - 技能列表
   * @param {number}  options.defense     - 防御值（0-100）
   * @param {number}  options.jumpHeight  - 弹跳高度（m）
   */
  constructor(o) {
    this.volume      = o.volume      ?? 1;
    this.movable     = o.movable     ?? true;
    this.speed       = o.speed       ?? 0;
    this.energyCost  = o.energyCost  ?? 10;
    this.skills      = o.skills      ?? [];
    this.defense     = o.defense     ?? 0;
    this.jumpHeight  = o.jumpHeight  ?? 0;
  }

  /**
   * 返回机器人属性摘要（调试 / UI 展示用）
   * @returns {string}
   */
  info() {
    return "体积:" + this.volume +
           " 可移动:" + this.movable +
           " 速度:" + this.speed +
           " 耗能:" + this.energyCost +
           " 技能:[" + this.skills.join(", ") + "]" +
           " 防御:" + this.defense +
           " 弹跳:" + this.jumpHeight;
  }
}