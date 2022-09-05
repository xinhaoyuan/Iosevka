.PHONY: archive fonts clean

archive: fonts
	STEM="iosevka-xy-`date +%Y%m%d`"; IDS="$$(./xy-build-plans.py --mode=print-package-paths)"; cd dist/.super-ttc; tar zcvf ../$$STEM.tgz $$IDS; cd ..; ln -sf $$STEM.tgz latest.tgz

fonts: private-build-plans.toml
	npm install
	npm run build -- `./xy-build-plans.py --mode=print-build-targets`

clean:
	rm -rf dist

private-build-plans.toml: xy-build-plans.py
	./xy-build-plans.py --mode=generate-build-plans
