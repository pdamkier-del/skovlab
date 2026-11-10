const { chromium } = require("playwright");
const assert = require("node:assert/strict");
(async () => {
  const browser = await chromium.launch({
    executablePath:
      process.env.CHROMIUM_PATH ||
      (require("node:fs").existsSync("/usr/bin/chromium")
        ? "/usr/bin/chromium"
        : chromium.executablePath()),
    headless: true,
    args: ["--no-sandbox"],
  });
  const page = await browser.newPage({
      viewport: { width: 1440, height: 1100 },
    }),
    errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const settle = () => page.waitForTimeout(450),
    data = () =>
      page.locator("#plot").evaluate((el) =>
        el.data.map((t) => ({
          name: t.name,
          y: t.y,
          x: t.x,
          raw: t.customdata,
          type: t.type,
          z: t.z,
        })),
      ),
    setTime = async (v) => {
      await page.locator("#time").fill(String(v));
      await page.locator("#time").dispatchEvent("input");
      await settle();
    };
  try {
    await page.goto("http://127.0.0.1:8000/ec-flrw/");
    await page.waitForSelector("#plot .scatterlayer .trace");
    assert.match(await page.title(), /EC Collapse Laboratory/);
    assert.match(await page.locator("#outcome").innerText(), /Bounce/);
    assert.equal(await page.locator("#H0").isDisabled(), true);
    assert.ok(
      Math.abs(+(await page.locator("#H0").inputValue()) + Math.sqrt(0.9)) <
        1e-10,
    );
    assert.equal((await data()).length, 2);
    assert.ok((await data())[1].y.some((y) => y < 0.11));
    await page.locator("#speed").selectOption(".25");
    await page.locator("#play").click();
    await page.waitForTimeout(400);
    await page.locator("#play").click();
    assert.notEqual(await page.locator("#clock").innerText(), "τ = 0");
    await setTime(250);
    const clock = await page.locator("#clock").innerText();
    assert.match(await page.locator("#liveState").innerText(), /Contracting/);
    const radius = +(await page.locator("#matterSphere").getAttribute("r"));
    assert.ok(radius > 0);
    await page.locator("#progressive").check();
    await settle();
    assert.ok((await data())[0].y.some((y) => y === null));
    await page.locator("[data-section=horizons]").click();
    await settle();
    assert.equal(await page.locator("#clock").innerText(), clock);
    assert.ok((await data())[0].y.some((y) => y < 0));
    await page.locator("#graph").selectOption("regions");
    await settle();
    let traces = await data();
    assert.equal(traces[0].type, "heatmap");
    assert.ok(traces[0].z.flat().some((z) => z === 1));
    assert.ok(traces[0].z.flat().some((z) => z === null));
    await page.locator("#progressive").uncheck();
    await settle();
    assert.ok((await data())[0].z.flat().some((z) => z === 2));
    assert.match(
      await page.locator("#plotNote").innerText(),
      /not an event horizon/,
    );
    await page
      .locator("#events button")
      .filter({ hasText: "Candidate bounce" })
      .click();
    await settle();
    assert.match(
      await page.locator("#eventDetail").innerText(),
      /Bounce inequality margin/,
    );
    assert.match(await page.locator("#liveState").innerText(), /Stationary/);
    assert.ok(
      +(await page.locator("#matterSphere").getAttribute("r")) < radius,
    );
    await page.locator("#validate").click();
    assert.match(await page.locator("#validation").innerText(), /^PASS/);
    await page.locator("#graph").selectOption("compactness");
    await settle();
    await page.locator("#compare").check();
    await settle();
    assert.equal((await data()).length, 2);
    assert.match(
      await page.locator("#comparisonNote").innerText(),
      /Hᵢ differs/,
    );
    await setTime(900);
    assert.match(
      await page.locator("#referenceState").innerText(),
      /No extrapolation/,
    );
    await page.locator("#match").selectOption("velocity");
    await settle();
    assert.match(
      await page.locator("#comparisonNote").innerText(),
      /ordinary density differs/,
    );
    await page.locator("#compare").uncheck();
    await page.locator("[data-section=matter]").click();
    await settle();
    assert.equal((await data()).length, 3);
    assert.equal(await page.locator("#scale").inputValue(), "signedlog");
    for (const t of await data())
      for (let i = 0; i < t.y.length; i++)
        assert.ok(
          Math.abs(
            t.y[i] -
              Math.sign(t.raw[i]) * Math.log10(1 + Math.abs(t.raw[i]) / 0.01),
          ) < 1e-10,
        );
    await page.locator("#graph").selectOption("pressure");
    await page.locator("#scale").selectOption("log");
    await settle();
    assert.match(
      await page.locator("#plotNote").innerText(),
      /nonpositive samples are omitted/,
    );
    await page.locator("#mode").selectOption("research");
    assert.equal(await page.locator("#Lkm").isVisible(), true);
    await page.locator("#Lkm").fill("10");
    await settle();
    assert.match(
      await page.locator("#physicalScale").innerText(),
      /Chosen L\*=10 km/,
    );
    await page.locator("#constraint").selectOption("velocity");
    await settle();
    assert.equal(await page.locator("#rho").isDisabled(), true);
    await page.locator("#H0").fill("-.5");
    await settle();
    assert.ok(
      Math.abs(+(await page.locator("#rho").inputValue()) - 1.05) < 1e-10,
    );
    await page.locator("#boundary").selectOption("physical");
    await page.locator("#R0").fill(".7");
    await settle();
    assert.match(await page.locator("#boundaryNote").innerText(), /= 0.7/);
    await page.locator("#reset").click();
    await settle();
    await page.locator("#k").selectOption("1");
    await settle();
    assert.match(await page.locator("#warnings").innerText(), /Inadmissible/);
    assert.equal((await page.locator("#plot").innerHTML()).length, 0);
    await page.locator("#rho").fill("6");
    await page.locator("#rb").fill(".5");
    await settle();
    assert.match(await page.locator("#equationLabel").innerText(), /k=1/);
    await page.locator("#preset").selectOption("reference");
    await settle();
    assert.equal(await page.locator("#constraint").inputValue(), "velocity");
    assert.ok(
      Math.abs(+(await page.locator("#rho").inputValue()) - 6.66) < 1e-10,
    );
    assert.match(await page.locator("#outcome").innerText(), /Bounce/);
    await page.locator("#reset").click();
    await settle();
    const jsonPromise = page.waitForEvent("download");
    await page.locator("#exportJSON").click();
    const jsonDownload = await jsonPromise;
    assert.equal(jsonDownload.suggestedFilename(), "ec-collapse-run.json");
    const fs = require("node:fs");
    const record = JSON.parse(
      fs.readFileSync(await jsonDownload.path(), "utf8"),
    );
    assert.equal(record.run.p.theory, "ec");
    assert.ok(record.run.assumptions.equations.includes("Hashemi"));
    assert.ok(record.run.events.some((e) => e.kind === "bounce"));
    const csvPromise = page.waitForEvent("download");
    await page.locator("#exportCSV").click();
    assert.equal((await csvPromise).suggestedFilename(), "ec-collapse-ec.csv");
    await page.locator("[data-section=research]").click();
    await page.locator("#saveRun").click();
    await page.locator("#spin2").fill(".6");
    await settle();
    await page.locator("#showSaved").check();
    await settle();
    assert.equal((await data()).length, 4);
    assert.match(
      await page.locator("#comparisonNote").innerText(),
      /Saved reference/,
    );
    await page.locator("#showSaved").uncheck();
    await page.locator("#runSweep").click();
    await page.waitForFunction(() =>
      document
        .getElementById("sweepStatus")
        .textContent.includes("25 cases completed"),
    );
    assert.ok(
      await page
        .locator("#sweepPlot")
        .evaluate((el) => el.data[0].x.length === 25),
    );
    const sweepPromise = page.waitForEvent("download");
    await page.locator("#exportSweep").click();
    assert.equal(
      (await sweepPromise).suggestedFilename(),
      "ec-collapse-screen.json",
    );
    await page.locator("#sweepN").selectOption("8");
    await page.locator("#runSweep").click();
    await page.locator("#cancelSweep").click();
    assert.match(await page.locator("#sweepStatus").innerText(), /cancelled/);
    await page.reload();
    await page.waitForSelector("#plot .scatterlayer .trace");
    assert.equal(await page.locator("#mode").inputValue(), "research");
    assert.equal(await page.locator("#spin2").inputValue(), "0.6");
    await page.locator("#preset").selectOption("gr");
    await settle();
    assert.equal(await page.locator("#spin2").isDisabled(), true);
    assert.match(await page.locator("#outcome").innerText(), /unresolved/);
    assert.match(
      await page.locator("#warnings").innerText(),
      /threshold|unresolved/,
    );
    await page.locator("#validate").click();
    assert.match(
      await page.locator("#validation").innerText(),
      /^NOT ESTABLISHED/,
    );
    await page.locator("#reset").click();
    await settle();
    await page
      .locator("#plot")
      .evaluate((el) =>
        Plotly.relayout(el, { "xaxis.range": [0.3, 0.7], dragmode: "pan" }),
      );
    await page.locator("#resetView").click();
    await settle();
    assert.equal(
      await page.locator("#plot").evaluate((el) => el.layout.xaxis.autorange),
      true,
    );
    await page.locator("#plot .legend .traces").first().click();
    await settle();
    assert.equal(
      await page.locator("#plot").evaluate((el) => el.data[0].visible),
      "legendonly",
    );
    await page.locator("#plot .legend .traces").first().click();
    const box = await page.locator("#plot").boundingBox();
    await page.mouse.move(box.x + box.width * 0.4, box.y + 130);
    await settle();
    assert.ok(await page.locator("#plot .hoverlayer").innerHTML());
    for (const width of [390, 720, 1024]) {
      await page.setViewportSize({ width, height: 844 });
      await settle();
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth,
        ),
        false,
        `horizontal overflow at ${width}`,
      );
      await page.locator("[data-section=horizons]").click();
      await page.locator("#graph").selectOption("regions");
      await settle();
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth,
        ),
        false,
        `map overflow at ${width}`,
      );
      await page.locator("[data-section=collapse]").click();
    }
    assert.equal(await page.locator(".scope button:disabled").count(), 2);
    assert.deepEqual(errors, []);
    console.log(
      "EC Collapse Laboratory browser checks passed: constrained inputs, bounce/trapping events, shared playback, progressive traces, maps, GR/EC matching, saved runs, exports, worker screen/cancellation, failure states and responsive layouts.",
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
