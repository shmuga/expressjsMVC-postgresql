


################################################################################
# VARIABLES
################################################################################


# PROJECT PATHS ################################################################

PROJECT_PATH        ?= $(shell pwd)
CONFIG_PATH         ?= $(PROJECT_PATH)/etc/build
TEMPLATES_PATH      ?= $(CONFIG_PATH)/templates
SOURCES_LISTS_PATH  ?= $(CONFIG_PATH)/sources-lists
JS_BUILD_PATH       ?= $(PROJECT_PATH)/public/js
JS_EXTERNS_PATH     ?= $(PROJECT_PATH)/externs
JS_SOURCES_PATH     ?= $(PROJECT_PATH)/lib
CSS_BUILD_PATH      ?= $(PROJECT_PATH)/public/css
CSS_SOURCES_PATH    ?= $(PROJECT_PATH)/styles
MODULES_PATH        ?= $(PROJECT_PATH)/node_modules
TOOLS_PATH          ?= $(MODULES_PATH)/livetex-tools
ENV_EXTERNS_PATH    ?= $(TOOLS_PATH)/externs


# ENVIRONMENT ##################################################################

JS_ENVIRONMENT      ?= browser


# AUX VARS #####################################################################

CSS_TEMPLATES       ?= $(foreach FILE, \
                       $(shell find $(TEMPLATES_PATH)/css -maxdepth 1 \
                       -iname '*.csst'), \
                       $(shell basename $(FILE) | cut -d '.' -f 1))


# PREREQUISITES PATHS ##########################################################

vpath %.csst        $(TEMPLATES_PATH)/css
vpath %.cssd        $(SOURCES_LISTS_PATH)/css
vpath %.css         $(CSS_BUILD_PATH)


################################################################################
# TOOLS
################################################################################

CSS_COMPILER ?= java -jar $(TOOLS_PATH)/tools/closure-stylesheets.jar


################################################################################
# RULES
################################################################################

################################################################################
# AUX RULES ####################################################################


# COMPILATIONS #################################################################

%.css-compile: %.cssd
	$(CSS_COMPILER) $(foreach FILE, $(shell cat $<), $(CSS_SOURCES_PATH)/$(FILE))


#################################################################### AUX RULES #
################################################################################


################################################################################
# MAIN RULES ###################################################################

%.css-assemble: %.csst
	@mkdir -p $(CSS_BUILD_PATH)
	$(TEMPLATER) $< > \
	$(shell echo $(CSS_BUILD_PATH)/$(shell basename $<) | cut -d '.' -f 1).css


################################################################### MAIN RULES #
################################################################################


################################################################################
# GENERAL RULES ################################################################


css: css-build
	@echo $@: DONE


css-clean:
	@#rm -rf $(wildcard $(CSS_BUILD_PATH)/*.css)
	@rm -rf $(shell find $(CSS_BUILD_PATH) -maxdepth 1 \
	-not -name mobile-invite.css -not -name css)
	@echo $@: DONE


css-build: css-clean
	@mkdir -p $(CSS_BUILD_PATH)
	@$(foreach TARGET_NAME, $(CSS_TEMPLATES), make -s $(shell echo \
  $(MAKE) -s $(shell echo $(TARGET_NAME).css-assemble);)
  @echo $@: DONE


################################################################ GENERAL RULES #
################################################################################
